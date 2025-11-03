from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set

import yaml
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from database import ApiRegistry, ComponentRegistry, db_session


VENDOR_PROPERTIES_KEY = "x-deepmock-properties"


@dataclass
class ComponentSummary:
    component_name: str
    storage_key: str
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


def _build_storage_key(api_slug: str, component_name: str) -> str:
    base = f"{api_slug}_{slugify(component_name)}"
    # PostgreSQL identifiers are limited to 63 characters.
    return base[:63]


def _prepare_component_rows(schema: Dict[str, Any]) -> list[Dict[str, Any]]:
    properties: Dict[str, Any] = schema.get("properties", {}) or {}
    required: Iterable[str] = schema.get("required", []) or []
    required_set = set(required)
    rows: list[Dict[str, Any]] = []

    for idx, (prop_name, definition) in enumerate(properties.items(), start=1):
        if not isinstance(definition, dict):
            definition = {"description": str(definition)}

        prop_type = definition.get("type")
        if not prop_type and "$ref" in definition:
            prop_type = "ref"

        rows.append(
            {
                "position": idx,
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
        with db_session() as session:
            original_title = info.get("title") or derived_name
            _persist_api_registry(session, api_slug, derived_name, original_title, version)
            for component_name, schema in schemas.items():
                normalized_schema = schema if isinstance(schema, dict) else {"definition": schema}
                storage_key = _build_storage_key(api_slug, component_name)
                property_rows = _prepare_component_rows(normalized_schema)
                enriched_schema = dict(normalized_schema)
                enriched_schema[VENDOR_PROPERTIES_KEY] = property_rows
                _persist_component_registry(session, api_slug, component_name, storage_key, enriched_schema)
                summaries.append(
                    ComponentSummary(
                        component_name=component_name,
                        storage_key=storage_key,
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


def _extract_properties_from_schema(schema: Any) -> list[Dict[str, Any]]:
    if isinstance(schema, dict):
        properties = schema.get(VENDOR_PROPERTIES_KEY)
        if isinstance(properties, list):
            return properties
        return _prepare_component_rows(schema)
    return []


def _persist_api_registry(
    session: Session,
    api_slug: str,
    api_name: str,
    title: str,
    version: Optional[str],
) -> None:
    existing = session.exec(
        select(ApiRegistry).where(ApiRegistry.api_slug == api_slug)
    ).first()
    if existing:
        existing.api_name = api_name
        existing.title = title
        existing.version = version
    else:
        session.add(
            ApiRegistry(
                api_slug=api_slug,
                api_name=api_name,
                title=title,
                version=version,
            )
        )


def _persist_component_registry(
    session: Session,
    api_slug: str,
    component_name: str,
    storage_key: str,
    schema: Any,
) -> None:
    existing = session.exec(
        select(ComponentRegistry)
        .where(ComponentRegistry.api_slug == api_slug)
        .where(ComponentRegistry.component_name == component_name)
    ).first()
    if existing:
        existing.table_name = storage_key
        existing.schema_payload = schema
    else:
        session.add(
            ComponentRegistry(
                api_slug=api_slug,
                component_name=component_name,
                table_name=storage_key,
                schema_payload=schema,
            )
        )


def list_apis() -> list[Dict[str, Any]]:
    with db_session() as session:
        apis = session.exec(
            select(ApiRegistry).order_by(ApiRegistry.api_name.asc())
        ).all()
        return [
            {
                "api_slug": api.api_slug,
                "api_name": api.api_name,
                "title": api.title,
                "version": api.version,
                "created_at": api.created_at,
            }
            for api in apis
        ]


def list_components(api_slug: str) -> list[Dict[str, Any]]:
    with db_session() as session:
        records = session.exec(
            select(ComponentRegistry)
            .where(ComponentRegistry.api_slug == api_slug)
            .order_by(ComponentRegistry.component_name.asc())
        ).all()
        components: list[Dict[str, Any]] = []
        for record in records:
            properties = _extract_properties_from_schema(record.schema_payload)
            components.append(
                {
                    "component_name": record.component_name,
                    "storage_key": record.table_name,
                    "created_at": record.created_at,
                    "property_count": len(properties),
                }
            )
        return components


def get_component_entry(api_slug: str, component_name: str) -> Optional[Dict[str, Any]]:
    with db_session() as session:
        record = session.exec(
            select(ComponentRegistry)
            .where(ComponentRegistry.api_slug == api_slug)
            .where(ComponentRegistry.component_name == component_name)
        ).first()

    if not record:
        return None


    return {
        "api_slug": record.api_slug,
        "component_name": record.component_name,
        "table_name": record.table_name,
        "storage_key": record.table_name,
        "schema": record.schema_payload,
        "created_at": record.created_at,
    }

def get_component_properties(entry: Dict[str, Any]) -> list[Dict[str, Any]]:
    schema = entry.get("schema")
    return _extract_properties_from_schema(schema)


def construct_component_graph(api_slug: str) -> Dict[str, Any]:
    import sys
    import os
    
    with db_session() as session:
        # Debug: Print database connection info
        db_url = os.getenv("_DATABASE_URL", "NOT SET")
        db_info = db_url.split('@')[-1] if '@' in db_url else db_url
        print(f"[construct_component_graph] Connecting to database: {db_info}", file=sys.stderr)
        
        # Debug: Print all component records to see what's in THIS database
        all_records = session.exec(select(ComponentRegistry)).all()
        api_slugs = {record.api_slug for record in all_records}
        print(f"[construct_component_graph] ComponentRegistry contains {len(all_records)} total records", file=sys.stderr)
        print(f"[construct_component_graph] API slugs in ComponentRegistry: {api_slugs}", file=sys.stderr)
        
        if not api_slugs:
            print(f"[construct_component_graph] WARNING: ComponentRegistry is EMPTY in this database!", file=sys.stderr)
            print(f"[construct_component_graph] This database ({db_info}) doesn't have components.", file=sys.stderr)
            print(f"[construct_component_graph] Use --shared-database-url to point to your main database.", file=sys.stderr)
        
        # Query for specific API slug
        records = session.exec(
            select(ComponentRegistry)
            .where(ComponentRegistry.api_slug == api_slug)
        ).all()
        
        print(f"[construct_component_graph] Query for api_slug='{api_slug}': found {len(records)} records", file=sys.stderr)
    if not records:
        # Check if API exists in api_registry but has no components
        from database import ApiRegistry
        with db_session() as check_session:
            api_exists = check_session.exec(
                select(ApiRegistry).where(ApiRegistry.api_slug == api_slug)
            ).first()
        
        if api_exists:
            raise ValueError(
                f"API '{api_slug}' exists in registry but has no components. "
                f"Components must be loaded via /apis/upload. "
                f"The OpenAPI spec must include a 'components.schemas' section."
            )
        else:
            raise ValueError(f"API '{api_slug}' not found. Upload OpenAPI spec via /apis/upload first.")

    component_names = {record.component_name for record in records}
    adjacency: Dict[str, Set[str]] = {name: set() for name in component_names}
    nodes: list[Dict[str, Any]] = []

    for record in records:
        schema = record.schema_payload if isinstance(record.schema_payload, dict) else {}
        properties = _extract_properties_from_schema(schema)
        refs = _collect_component_refs(schema)
        filtered_refs = {ref for ref in refs if ref in component_names and ref != record.component_name}
        adjacency[record.component_name].update(filtered_refs)
        nodes.append(
            {
                "component_name": record.component_name,
                "storage_key": record.table_name,
                "created_at": record.created_at,
                "property_count": len(properties),
            }
        )

    edges: list[Dict[str, str]] = []
    dependents: Dict[str, int] = {name: 0 for name in component_names}
    for source, targets in adjacency.items():
        for target in sorted(targets):
            edges.append({"source": source, "target": target})
            dependents[target] += 1

    for node in nodes:
        name = node["component_name"]
        node["references"] = sorted(adjacency.get(name, set()))
        node["dependent_count"] = dependents.get(name, 0)

    return {
        "nodes": nodes,
        "edges": edges,
    }


def _collect_component_refs(payload: Any) -> Set[str]:
    refs: Set[str] = set()
    if isinstance(payload, dict):
        ref_value = payload.get("$ref")
        if isinstance(ref_value, str):
            resolved = _normalise_schema_ref(ref_value)
            if resolved:
                refs.add(resolved)
        for value in payload.values():
            refs.update(_collect_component_refs(value))
    elif isinstance(payload, list):
        for item in payload:
            refs.update(_collect_component_refs(item))
    return refs


def _normalise_schema_ref(ref: str) -> Optional[str]:
    if not isinstance(ref, str):
        return None
    if ref.startswith("#/components/schemas/"):
        return ref.split("/")[-1]
    # Ignore external refs or other component categories for now.
    return None
