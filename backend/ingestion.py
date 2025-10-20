from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    MetaData,
    RowMapping,
    String,
    Table,
    Text,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB, insert as pg_insert
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from database import api_registry, component_registry, db_connection, get_engine


@dataclass
class ComponentSummary:
    component_name: str
    table_name: str
    property_count: int


@dataclass
class IngestionResult:
    api_slug: str
    api_name: str
    version: Optional[str]
    components: list[ComponentSummary]


def slugify(value: str) -> str:
    """Convert an arbitrary string into a safe PostgreSQL identifier fragment."""
    lowered = value.lower()
    sanitized = "".join(ch if ch.isalnum() else "_" for ch in lowered)
    while "__" in sanitized:
        sanitized = sanitized.replace("__", "_")
    return sanitized.strip("_") or "api"


def parse_openapi_spec(raw_spec: str) -> Dict[str, Any]:
    try:
        parsed = yaml.safe_load(raw_spec)
    except yaml.YAMLError as exc:  # pragma: no cover - top-level parse errors are surfaced to caller
        raise ValueError(f"Unable to parse OpenAPI spec: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("OpenAPI spec must deserialize into a dictionary.")
    return parsed


def _build_table_name(api_slug: str, component_name: str) -> str:
    base = f"{api_slug}_{slugify(component_name)}"
    # PostgreSQL identifiers are limited to 63 characters.
    return base[:63]


def _prepare_component_rows(schema: Dict[str, Any]) -> list[Dict[str, Any]]:
    properties: Dict[str, Any] = schema.get("properties", {}) or {}
    required: Iterable[str] = schema.get("required", []) or []
    required_set = set(required)
    rows: list[Dict[str, Any]] = []

    for prop_name, definition in properties.items():
        if not isinstance(definition, dict):
            definition = {"description": str(definition)}

        prop_type = definition.get("type")
        if not prop_type and "$ref" in definition:
            prop_type = "ref"

        rows.append(
            {
                "property_name": prop_name,
                "property_type": prop_type,
                "property_format": definition.get("format"),
                "is_required": prop_name in required_set,
                "description": definition.get("description"),
                "example": definition.get("example"),
                "reference": definition.get("$ref"),
            }
        )

    return rows


def ingest_openapi_spec(raw_spec: str, *, explicit_name: Optional[str] = None) -> IngestionResult:
    spec = parse_openapi_spec(raw_spec)
    info = spec.get("info", {}) or {}
    derived_name = explicit_name or info.get("title")
    if not derived_name:
        raise ValueError("OpenAPI spec must include info.title or an explicit name must be supplied.")

    api_slug = slugify(derived_name)
    version = info.get("version")

    components = spec.get("components", {}) or {}
    schemas: Dict[str, Any] = components.get("schemas", {}) or {}
    if not schemas:
        raise ValueError("OpenAPI file does not define any components.schemas to ingest.")

    summaries: list[ComponentSummary] = []
    try:
        with db_connection() as conn:
            original_title = info.get("title") or derived_name
            _persist_api_registry(conn, api_slug, derived_name, original_title, version)
            for component_name, schema in schemas.items():
                normalized_schema = schema if isinstance(schema, dict) else {"definition": schema}
                table_name = _build_table_name(api_slug, component_name)
                property_rows = _prepare_component_rows(normalized_schema)
                component_table = _create_component_table(table_name)
                if property_rows:
                    conn.execute(component_table.insert(), property_rows)
                _persist_component_registry(conn, api_slug, component_name, table_name, normalized_schema)
                summaries.append(
                    ComponentSummary(
                        component_name=component_name,
                        table_name=table_name,
                        property_count=len(property_rows),
                    )
                )
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while ingesting spec: {exc}") from exc

    return IngestionResult(
        api_slug=api_slug,
        api_name=derived_name,
        version=version,
        components=summaries,
    )


def _persist_api_registry(
    conn: Connection,
    api_slug: str,
    api_name: str,
    title: str,
    version: Optional[str],
) -> None:
    stmt = pg_insert(api_registry).values(
        api_slug=api_slug,
        api_name=api_name,
        title=title,
        version=version,
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[api_registry.c.api_slug],
        set_={
            "api_name": api_name,
            "title": title,
            "version": version,
        },
    )
    conn.execute(stmt)


def _persist_component_registry(
    conn: Connection,
    api_slug: str,
    component_name: str,
    table_name: str,
    schema: Any,
) -> None:
    stmt = pg_insert(component_registry).values(
        api_slug=api_slug,
        component_name=component_name,
        table_name=table_name,
        schema=schema,
    )
    stmt = stmt.on_conflict_do_update(
        constraint="uq_component_registry_slug_component",
        set_={
            "table_name": table_name,
            "schema": schema,
        },
    )
    conn.execute(stmt)


def _create_component_table(table_name: str) -> Table:
    """Drop and (re)create the component table using autocommit DDL.

    Executing DDL outside the main ingestion transaction avoids exhausting
    Postgres max_locks_per_transaction when many components are processed.
    """
    metadata = MetaData()
    component_table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("property_name", String(200), nullable=False),
        Column("property_type", String(100)),
        Column("property_format", String(100)),
        Column("is_required", Boolean, nullable=False, default=False),
        Column("description", Text),
        Column("example", JSONB),
        Column("reference", String(255)),
    )

    engine = get_engine()
    # Perform DDL in autocommit to prevent accumulating locks in one tx
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as ddl_conn:
        component_table.drop(bind=ddl_conn, checkfirst=True)
        component_table.create(bind=ddl_conn)

    return component_table


def list_apis() -> list[Dict[str, Any]]:
    with db_connection() as conn:
        result = conn.execute(
            select(
                api_registry.c.api_slug,
                api_registry.c.api_name,
                api_registry.c.title,
                api_registry.c.version,
                api_registry.c.created_at,
            ).order_by(api_registry.c.api_name.asc())
        )
        return [dict(row._mapping) for row in result.fetchall()]


def list_components(api_slug: str) -> list[Dict[str, Any]]:
    with db_connection() as conn:
        result = conn.execute(
            select(
                component_registry.c.component_name,
                component_registry.c.table_name,
                component_registry.c.created_at,
            )
            .where(component_registry.c.api_slug == api_slug)
            .order_by(component_registry.c.component_name.asc())
        )
        return [dict(row._mapping) for row in result.fetchall()]


def fetch_component_rows(table_name: str) -> list[Dict[str, Any]]:
    engine = get_engine()
    metadata = MetaData()
    component_table = Table(table_name, metadata, autoload_with=engine)
    with db_connection() as conn:
        result = conn.execute(select(component_table).order_by(component_table.c.property_name.asc())).fetchall()
    return [dict(row._mapping) for row in result]


def get_component_entry(api_slug: str, component_name: str) -> Optional[Dict[str, Any]]:
    with db_connection() as conn:
        result = conn.execute(
            select(component_registry)
            .where(component_registry.c.api_slug == api_slug)
            .where(component_registry.c.component_name == component_name)
        ).first()

    if not result:
        return None
    mapping: RowMapping = result._mapping
    return dict(mapping)
