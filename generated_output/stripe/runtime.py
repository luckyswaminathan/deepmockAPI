"""Standalone in-memory runtime for the Stripe API mock."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

# In-memory storage: {component_name: [records]}
_storage: Dict[str, list[Dict[str, Any]]] = {}


def fetch_component_records(api_slug: str, component_name: str) -> list[dict[str, Any]]:
    """Fetch all records for a component."""
    return _storage.get(component_name, []).copy()


def fetch_component_record(
    api_slug: str, component_name: str, field: str, value: Any
) -> Optional[dict[str, Any]]:
    """Fetch a single record by field value."""
    records = _storage.get(component_name, [])
    for record in records:
        if str(record.get(field)) == str(value):
            return record.copy()
        if str(record.get("id")) == str(value):
            return record.copy()
    return None


def insert_component_record(api_slug: str, component_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Insert or update a record."""
    record = dict(payload)
    key = _derive_record_key(record)
    record.setdefault("id", key)
    
    if component_name not in _storage:
        _storage[component_name] = []
    
    # Check if record exists by key/id
    records = _storage[component_name]
    for i, existing_record in enumerate(records):
        existing_key = existing_record.get("id") or _derive_record_key(existing_record)
        if existing_key == key:
            # Update existing
            records[i] = record
            return record.copy()
    
    # Add new record
    records.append(record)
    return record.copy()


def update_component_record(
    api_slug: str,
    component_name: str,
    field: str,
    value: Any,
    payload: dict[str, Any],
) -> Optional[dict[str, Any]]:
    """Update a record by field value."""
    if component_name not in _storage:
        return None
    
    records = _storage[component_name]
    key = str(value)
    
    for i, record in enumerate(records):
        if str(record.get(field)) == key or str(record.get("id")) == key:
            merged = dict(record)
            merged.update(payload)
            merged[field] = merged.get(field, key)
            merged.setdefault("id", merged.get(field, key))
            records[i] = merged
            return merged.copy()
    
    return None


def delete_component_record(api_slug: str, component_name: str, field: str, value: Any) -> bool:
    """Delete a record by field value."""
    if component_name not in _storage:
        return False
    
    records = _storage[component_name]
    key = str(value)
    
    for i, record in enumerate(records):
        if str(record.get(field)) == key or str(record.get("id")) == key:
            del records[i]
            return True
    
    return False


def replace_dataset(api_slug: str, dataset: Dict[str, list[dict[str, Any]]]) -> None:
    """Replace all data with a new dataset."""
    global _storage
    _storage = {component_name: [dict(record) for record in records] 
                for component_name, records in dataset.items()}


def remove_dataset(api_slug: str) -> None:
    """Clear all data for an API."""
    global _storage
    _storage.clear()


def _derive_record_key(payload: dict[str, Any]) -> str:
    """Derive a key from a payload."""
    for candidate in ("id", "uuid", "uid", "key"):
        value = payload.get(candidate)
        if value is not None:
            return str(value)
    return str(uuid4())

