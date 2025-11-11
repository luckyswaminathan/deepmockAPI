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
    # FastAPI caches the OpenAPI schema after the first /docs request. Reset it so the new
    # generated routes become visible without forcing a server restart.
    if hasattr(app, "openapi_schema"):
        app.openapi_schema = None
    _mounted_routers.add(api_slug)


def replace_dataset(api_slug: str, dataset: Dict[str, list[dict[str, Any]]]) -> None:
    """
    Replace all generated records for an API in the GeneratedRecord table.
    
    This clears existing records and inserts all new records from the dataset.
    """
    import sys
    
    if not dataset:
        print(f"[runtime.replace_dataset] WARNING: Empty dataset for {api_slug}", file=sys.stderr)
        return
    
    print(f"[runtime.replace_dataset] Starting store for {api_slug} with {len(dataset)} components", file=sys.stderr)
    
    try:
        with db_session() as session:
            # Clear all existing records for this API
            deleted = session.exec(delete(GeneratedRecord).where(GeneratedRecord.api_slug == api_slug))
            print(f"[runtime.replace_dataset] Cleared existing records for {api_slug}", file=sys.stderr)
            
            # Add all new records from dataset
            total_added = 0
            for component_name, records in dataset.items():
                if not records:
                    continue
                component_count = len(records)
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
                    total_added += 1
                print(f"[runtime.replace_dataset] Added {component_count} records for component '{component_name}'", file=sys.stderr)
            
            # Explicit flush to ensure writes happen
            session.flush()
            print(f"[runtime.replace_dataset] Successfully stored {total_added} total records for {api_slug}", file=sys.stderr)
    except Exception as e:
        import traceback
        print(f"[runtime.replace_dataset] ERROR storing data for {api_slug}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

## TODO - need to update GeneratedRecord type doesn't seem right
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
            merged = dict(existing.payload)
            merged.update(record)
            # Preserve canonical id and record_key
            if "id" in existing.payload:
                merged["id"] = existing.payload["id"]
            existing.payload = merged
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
    last_error: Optional[Exception] = None
    for module_path in module_paths:
        try:
            # Temporarily patch sys.modules to help with runtime import
            # The generated routes try to import 'runtime' locally, but we want them
            # to use 'reverse.runtime' when imported as a module
            import sys
            original_runtime = sys.modules.get("runtime")
            
            # If runtime module doesn't exist, try to import reverse.runtime
            if "runtime" not in sys.modules:
                try:
                    from reverse import runtime as reverse_runtime
                    sys.modules["runtime"] = reverse_runtime
                except ImportError:
                    pass
            
            module = importlib.import_module(module_path)
            
            # Restore original runtime if it existed
            if original_runtime is not None:
                sys.modules["runtime"] = original_runtime
            elif "runtime" in sys.modules and original_runtime is None:
                # Only remove if we added it
                try:
                    del sys.modules["runtime"]
                except KeyError:
                    pass
            
            # Verify router exists
            if hasattr(module, "router"):
                return module
            else:
                raise RuntimeError(f"Module {module_path} does not have a 'router' attribute")
        except ModuleNotFoundError as exc:
            last_error = exc
        except Exception as exc:
            # Catch other import errors (syntax errors, etc.)
            last_error = exc
            import sys
            print(f"[runtime] Error importing {module_path}: {exc}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
    
    error_msg = f"Generated routes module not found for API slug '{api_slug}'. "
    error_msg += f"Tried: {', '.join(module_paths)}"
    if last_error:
        error_msg += f" Last error: {last_error}"
    raise RuntimeError(error_msg) from last_error


def discover_generated_apis() -> list[str]:
    """
    Discover all generated APIs by scanning the generated directory.
    
    Returns:
        List of API slugs that have generated routes.
    """
    from pathlib import Path
    
    # Check both possible locations
    possible_roots = [
        Path(__file__).parent / "generated",  # backend/reverse/generated
        Path(__file__).parent.parent / "generated_apis",  # backend/generated_apis
    ]
    
    api_slugs = []
    for root in possible_roots:
        if not root.exists():
            continue
        
        # Look for subdirectories with code/routes.py
        for item in root.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                routes_file = item / "code" / "routes.py"
                if routes_file.exists():
                    api_slugs.append(item.name)
                else:
                    # Also check generated_apis structure (routes.py directly)
                    alt_routes_file = item / "routes.py"
                    if alt_routes_file.exists():
                        api_slugs.append(item.name)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_slugs = []
    for slug in api_slugs:
        if slug not in seen:
            seen.add(slug)
            unique_slugs.append(slug)
    
    return unique_slugs


def _derive_record_key(payload: dict[str, Any]) -> str:
    for candidate in ("id", "uuid", "uid", "key"):
        value = payload.get(candidate)
        if value is not None:
            return str(value)
    return str(uuid4())
