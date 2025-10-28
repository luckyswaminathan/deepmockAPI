from __future__ import annotations

import importlib
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import FastAPI
from sqlmodel import delete, select

from database import GeneratedRecord, db_session
_mounted_routers: set[str] = set()


def mount_generated_routes(app: FastAPI, api_slug: str, *, prefix: Optional[str] = None) -> None:
    if api_slug in _mounted_routers:
        return

    module = _import_router_module(api_slug)

    router = getattr(module, "router", None)
    if router is None:
        raise RuntimeError(f"Generated routes module for '{api_slug}' does not expose a router.")

    app.include_router(router, prefix=prefix or f"/generated/{api_slug}")
    _mounted_routers.add(api_slug)


def replace_dataset(api_slug: str, dataset: Dict[str, list[dict[str, Any]]]) -> None:
    with db_session() as session:
        session.exec(delete(GeneratedRecord).where(GeneratedRecord.api_slug == api_slug))
        for component_name, records in dataset.items():
            session.exec(
                delete(GeneratedRecord)
                .where(GeneratedRecord.api_slug == api_slug)
                .where(GeneratedRecord.component_name == component_name)
            )
            for record in records:
                key = _derive_record_key(record)
                payload = dict(record)
                if "id" not in payload:
                    payload["id"] = key
                session.add(
                    GeneratedRecord(
                        api_slug=api_slug,
                        component_name=component_name,
                        record_key=key,
                        payload=payload,
                    )
                )


def fetch_component_records(api_slug: str, component_name: str) -> list[dict[str, Any]]:
    with db_session() as session:
        records = session.exec(
            select(GeneratedRecord)
            .where(GeneratedRecord.api_slug == api_slug)
            .where(GeneratedRecord.component_name == component_name)
            .order_by(GeneratedRecord.record_key.asc())
        ).all()
        return [record.payload for record in records]


def fetch_component_record(
    api_slug: str, component_name: str, field: str, value: Any
) -> Optional[dict[str, Any]]:
    records = fetch_component_records(api_slug, component_name)
    for record in records:
        if str(record.get(field)) == str(value):
            return record
        if str(record.get("id")) == str(value):
            return record
    return None


def insert_component_record(api_slug: str, component_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    record = dict(payload)
    key = _derive_record_key(record)
    record.setdefault("id", key)

    with db_session() as session:
        existing = session.exec(
            select(GeneratedRecord)
            .where(GeneratedRecord.api_slug == api_slug)
            .where(GeneratedRecord.component_name == component_name)
            .where(GeneratedRecord.record_key == key)
        ).first()

        if existing:
            existing.payload = record
        else:
            session.add(
                GeneratedRecord(
                    api_slug=api_slug,
                    component_name=component_name,
                    record_key=key,
                    payload=record,
                )
            )
    return record


def update_component_record(
    api_slug: str,
    component_name: str,
    field: str,
    value: Any,
    payload: dict[str, Any],
) -> Optional[dict[str, Any]]:
    key = str(value)
    with db_session() as session:
        records = session.exec(
            select(GeneratedRecord)
            .where(GeneratedRecord.api_slug == api_slug)
            .where(GeneratedRecord.component_name == component_name)
        ).all()

        target = None
        for record in records:
            if str(record.payload.get(field)) == key or record.record_key == key:
                target = record
                break

        if not target:
            return None

        merged = dict(target.payload)
        merged.update(payload)
        merged[field] = merged.get(field, key)
        merged.setdefault("id", merged[field])
        target.payload = merged
        target.record_key = str(merged.get(field, target.record_key))
        return merged


def delete_component_record(api_slug: str, component_name: str, field: str, value: Any) -> bool:
    key = str(value)
    with db_session() as session:
        records = session.exec(
            select(GeneratedRecord)
            .where(GeneratedRecord.api_slug == api_slug)
            .where(GeneratedRecord.component_name == component_name)
        ).all()

        for record in records:
            if str(record.payload.get(field)) == key or record.record_key == key:
                session.delete(record)
                return True
    return False


def remove_dataset(api_slug: str) -> None:
    with db_session() as session:
        session.exec(delete(GeneratedRecord).where(GeneratedRecord.api_slug == api_slug))


def _import_router_module(api_slug: str):
    module_paths = [
        f"generated_apis.{api_slug}.routes",
        f"reverse.generated.{api_slug}.code.routes",
    ]
    last_error: Optional[ModuleNotFoundError] = None
    for module_path in module_paths:
        try:
            return importlib.import_module(module_path)
        except ModuleNotFoundError as exc:
            last_error = exc
    raise RuntimeError(f"Generated routes module not found for API slug '{api_slug}'.") from last_error


def _derive_record_key(payload: dict[str, Any]) -> str:
    for candidate in ("id", "uuid", "uid", "key"):
        value = payload.get(candidate)
        if value is not None:
            return str(value)
    return str(uuid4())
