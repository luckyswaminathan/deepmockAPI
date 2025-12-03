from __future__ import annotations

import importlib
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import FastAPI
from sqlmodel import delete, select

from database import ComponentRegistry, GeneratedRecord, db_session
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
        # Merge each record with schema defaults
        return [_merge_with_schema_defaults(api_slug, component_name, record.payload) for record in records]


def fetch_component_record(
    api_slug: str, component_name: str, field: str, value: Any
) -> Optional[dict[str, Any]]:
    with db_session() as session:
        records = session.exec(
            select(GeneratedRecord)
            .where(GeneratedRecord.api_slug == api_slug)
            .where(GeneratedRecord.component_name == component_name)
        ).all()
        
        for db_record in records:
            payload = db_record.payload
            if str(payload.get(field)) == str(value) or str(payload.get("id")) == str(value):
                # Merge with schema defaults before returning
                return _merge_with_schema_defaults(api_slug, component_name, payload)
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
            stored_record = merged
        else:
            session.add(
                GeneratedRecord(
                    api_slug=api_slug,
                    component_name=component_name,
                    record_key=key,
                    payload=record,
                )
            )
            stored_record = record
    
    # Merge with schema defaults before returning
    return _merge_with_schema_defaults(api_slug, component_name, stored_record)


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
        
        # Merge with schema defaults before returning
        return _merge_with_schema_defaults(api_slug, component_name, merged)


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


def _extract_defaults_from_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract default values from OpenAPI schema.
    
    Recursively walks through schema properties and extracts default values.
    Includes ALL properties from the schema, using type-appropriate defaults when no explicit default exists.
    Skips additionalProperties.
    """
    defaults = {}
    
    if not isinstance(schema, dict):
        return defaults
    
    # Skip additionalProperties - these are dynamic and shouldn't have defaults
    if "additionalProperties" in schema:
        # Don't process additionalProperties as a regular property
        pass
    
    # Handle properties - include ALL properties, not just those with explicit defaults
    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        for prop_name, prop_schema in properties.items():
            if not isinstance(prop_schema, dict):
                continue
            
            # Skip properties that look like additionalProperties placeholders
            if prop_name.startswith("additionalProp"):
                continue
            
            # Check for explicit default value first
            if "default" in prop_schema:
                defaults[prop_name] = prop_schema["default"]
            # Handle nested objects - recurse to get nested defaults
            elif prop_schema.get("type") == "object":
                nested_defaults = _extract_defaults_from_schema(prop_schema)
                # Always include object, even if empty (use empty dict)
                defaults[prop_name] = nested_defaults if nested_defaults else {}
            # Handle arrays - use empty list as default
            elif prop_schema.get("type") == "array":
                defaults[prop_name] = []
            # Handle booleans - default to False
            elif prop_schema.get("type") == "boolean":
                defaults[prop_name] = False
            # Handle strings - use empty string, not null (unless nullable)
            elif prop_schema.get("type") == "string":
                if prop_schema.get("nullable", False):
                    defaults[prop_name] = None
                else:
                    defaults[prop_name] = ""
            # Handle numbers/integers - only set null if explicitly nullable
            elif prop_schema.get("type") in ["integer", "number"]:
                if prop_schema.get("nullable", False):
                    defaults[prop_name] = None
                # Don't set default for numbers - let them be missing
            # Handle nullable fields - set to None only if explicitly nullable
            elif prop_schema.get("nullable", False):
                defaults[prop_name] = None
            # For other types without explicit defaults, don't set a default
            # (let them be missing from defaults dict)
    
    return defaults


def _get_component_schema(api_slug: str, component_name: str) -> Optional[Dict[str, Any]]:
    """Get component schema from ComponentRegistry."""
    try:
        with db_session() as session:
            record = session.exec(
                select(ComponentRegistry)
                .where(ComponentRegistry.api_slug == api_slug)
                .where(ComponentRegistry.component_name == component_name)
            ).first()
            
            if record and record.schema_payload:
                return record.schema_payload
    except Exception:
        # If schema lookup fails, return None (graceful degradation)
        pass
    return None


def _merge_with_schema_defaults(
    api_slug: str, component_name: str, record: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge a record with schema defaults.
    
    Returns a new dict with all schema fields populated with defaults where missing.
    Preserves actual values from record, only fills in missing fields with defaults.
    """
    import sys
    
    schema = _get_component_schema(api_slug, component_name)
    if not schema:
        # If schema not found, return record as-is (graceful degradation)
        print(
            f"[runtime] Warning: Schema not found for {api_slug}/{component_name}, "
            f"returning record without defaults",
            file=sys.stderr
        )
        return record
    
    defaults = _extract_defaults_from_schema(schema)
    
    # Start with the actual record (preserve all existing values)
    merged = dict(record)
    
    # Only add defaults for fields that are missing from the record
    # Don't overwrite existing values (even if they're null - preserve user's data)
    for key, default_value in defaults.items():
        if key not in merged:
            merged[key] = default_value
        elif isinstance(merged[key], dict) and isinstance(default_value, dict):
            # Merge nested objects: start with defaults, overlay with record values
            nested_merged = default_value.copy()
            nested_merged.update(merged[key])
            merged[key] = nested_merged
    
    # Remove any additionalProp* keys that might have been added
    keys_to_remove = [k for k in merged.keys() if k.startswith("additionalProp")]
    for key in keys_to_remove:
        merged.pop(key, None)
    
    return merged
