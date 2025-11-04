"""Standalone in-memory runtime for the API mock."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

# In-memory storage: {component_name: [records]}
_storage: Dict[str, list[Dict[str, Any]]] = {}

# Per-account storage: {account_id: {component_name: [records]}}
_account_storage: Dict[str, Dict[str, list[Dict[str, Any]]]] = {}


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
    """Insert or update (upsert) a record via merge semantics.

    If a record with the same derived key exists, merge fields while preserving
    the existing 'id' and any unspecified fields. If no record exists, insert.
    """
    record = dict(payload)
    key = _derive_record_key(record)
    record.setdefault("id", key)
    
    if component_name not in _storage:
        _storage[component_name] = []
    
    records = _storage[component_name]
    for i, existing_record in enumerate(records):
        existing_key = existing_record.get("id") or _derive_record_key(existing_record)
        if existing_key == key:
            merged = dict(existing_record)
            merged.update(record)
            # Preserve canonical id from existing record
            if "id" in existing_record:
                merged["id"] = existing_record["id"]
            records[i] = merged
            return merged.copy()
    
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


# Account-scoped data operations
def fetch_account_component_records(
    account_id: str, component_name: str
) -> list[dict[str, Any]]:
    """Fetch records for a component scoped to a specific account."""
    account_data = _account_storage.get(account_id, {})
    return account_data.get(component_name, []).copy()


def fetch_account_component_record(
    account_id: str, component_name: str, field: str, value: Any
) -> Optional[dict[str, Any]]:
    """Fetch a single account-scoped record."""
    records = fetch_account_component_records(account_id, component_name)
    for record in records:
        if str(record.get(field)) == str(value):
            return record.copy()
        if str(record.get("id")) == str(value):
            return record.copy()
    return None


def insert_account_component_record(
    account_id: str, component_name: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Insert or update an account-scoped record."""
    if account_id not in _account_storage:
        _account_storage[account_id] = {}
    
    if component_name not in _account_storage[account_id]:
        _account_storage[account_id][component_name] = []
    
    record = dict(payload)
    key = _derive_record_key(record)
    record.setdefault("id", key)
    
    records = _account_storage[account_id][component_name]
    for i, existing_record in enumerate(records):
        existing_key = existing_record.get("id") or _derive_record_key(existing_record)
        if existing_key == key:
            records[i] = record
            return record.copy()
    
    records.append(record)
    return record.copy()


def replace_dataset(api_slug: str, dataset: Dict[str, list[dict[str, Any]]]) -> None:
    """Replace all data with a new dataset."""
    global _storage
    _storage = {{component_name: [dict(record) for record in records] 
                for component_name, records in dataset.items()}}


def remove_dataset(api_slug: str) -> None:
    """Clear all data for an API."""
    global _storage, _account_storage
    _storage.clear()
    _account_storage.clear()


def _derive_record_key(payload: dict[str, Any]) -> str:
    """Derive a stable upsert key from payload.

    Priority:
    1) Explicit 'record_key' if provided
    2) Account/customer scoped: f"{account}:{id}" or f"{customer}:{id}"
    3) First available among 'id', 'uuid', 'uid', 'key'
    4) New UUID4
    """
    # 1) Explicit record_key
    record_key = payload.get("record_key")
    if record_key is not None:
        return str(record_key)

    # 2) Scoped owner:id keys
    account = payload.get("account")
    customer = payload.get("customer")
    resource_id = payload.get("id")
    if resource_id is not None and (account is not None or customer is not None):
        owner = account if account is not None else customer
        return f"{owner}:{resource_id}"

    # 3) Fallback identifiers
    for candidate in ("id", "uuid", "uid", "key"):
        value = payload.get(candidate)
        if value is not None:
            return str(value)
    
    # 4) Last resort
    return str(uuid4())
