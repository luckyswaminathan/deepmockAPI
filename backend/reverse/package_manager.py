from __future__ import annotations

import shutil
from pathlib import Path
from reverse.storage import api_root, ensure_dir
from reverse import data_synthesizer


def packages_root() -> Path:
    root = Path(__file__).resolve().parent.parent / "generated_apis"
    ensure_dir(root)
    init_file = root / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Versioned packages for reverse-generated APIs."""\n\n__all__: list[str] = []\n', encoding="utf-8")
    return root


def sync_generated_package(api_slug: str) -> Path:
    source_root = api_root(api_slug)
    code_src = source_root / "code"
    tests_src = source_root / "tests"

    if not code_src.exists():
        raise FileNotFoundError(f"Generated code not found for API slug '{api_slug}'. Run /reverse/generate first.")

    root = packages_root()
    dest = root / api_slug

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(code_src, dest)
    _ensure_package(dest)

    if tests_src.exists():
        shutil.copytree(tests_src, dest / "tests")
        _ensure_package(dest / "tests")

    _update_package_index()
    return dest


def list_packages() -> list[str]:
    root = packages_root()
    return sorted(
        [
            entry.name
            for entry in root.iterdir()
            if entry.is_dir() and not entry.name.startswith("_")
        ]
    )


def sync_standalone_api(api_slug: str) -> Path:
    """
    Sync generated code to generated_output/{api_slug} with standalone API structure.
    
    Creates: main.py, runtime.py, requirements.txt, and seeds data.
    """
    source_root = api_root(api_slug)
    code_src = source_root / "code"
    plan_src = source_root / "plan"
    
    if not code_src.exists():
        raise FileNotFoundError(f"Generated code not found for API slug '{api_slug}'. Run /reverse/generate first.")
    
    # Target: generated_output/{api_slug}/
    # Check for OUTPUT_DIR environment variable first (used by Docker scripts)
    # Then try relative to backend directory, then relative to repo root
    import os
    output_root_env = os.getenv("OUTPUT_DIR") or os.getenv("GENERATED_OUTPUT_DIR")
    if output_root_env:
        output_root = Path(output_root_env)
    else:
        # Calculate relative to backend directory: backend/reverse/package_manager.py -> backend/ -> repo_root/generated_output
        backend_dir = Path(__file__).resolve().parent.parent.parent
        # Check if we're in backend/ directory structure
        if backend_dir.name == "backend":
            output_root = backend_dir.parent / "generated_output"
        else:
            # Fallback: assume generated_output is sibling to backend
            output_root = Path(__file__).resolve().parent.parent.parent / "generated_output"
    
    ensure_dir(output_root)
    dest = output_root / api_slug
    ensure_dir(dest)
    print(f"[sync_standalone_api] Writing to: {dest}", file=__import__("sys").stderr)
    
    # Copy code
    code_dest = dest / "code"
    if code_dest.exists():
        shutil.rmtree(code_dest)
    shutil.copytree(code_src, code_dest)
    
    # Fix imports in routes.py for standalone API
    routes_file = code_dest / "routes.py"
    if routes_file.exists():
        content = routes_file.read_text(encoding="utf-8")
        # Replace backend import with local runtime import
        if "from reverse import runtime as generated_runtime" in content:
            replacement = '''# Import local runtime module from parent directory
import sys
from pathlib import Path

# Add parent directory to Python path to import runtime
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import runtime as generated_runtime'''
            content = content.replace(
                "from reverse import runtime as generated_runtime",
                replacement
            )
            routes_file.write_text(content, encoding="utf-8")
    
    # Copy plan if exists
    if plan_src.exists():
        plan_dest = dest / "plan"
        if plan_dest.exists():
            shutil.rmtree(plan_dest)
        shutil.copytree(plan_src, plan_dest)
    
    # Create standalone API files if they don't exist
    # This MUST happen before data generation so files exist even if data generation fails
    try:
        _ensure_standalone_files(dest, api_slug)
        print(f"[sync_standalone_api] Created standalone files: main.py, runtime.py, requirements.txt", file=__import__("sys").stderr)
    except Exception as e:
        import sys
        import traceback
        print(f"[sync_standalone_api] ERROR: Failed to create standalone files: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise  # Re-raise because we MUST have these files
    
    # Generate and seed data using graph-based generator
    try:
        # Generate data for ALL components using dependency graph
        # Default: 3 records per component (can be customized via API)
        dataset = data_synthesizer.synthesize_all_components(
            api_slug,
            count_per_component=None,  # Uses default of 3 per component
            seed_account_id=None,
        )
        
        # Write seed data JSON file
        import json
        from datetime import datetime, timezone
        
        seed_file = dest / "data" / "seeds" / "generated.json"
        ensure_dir(seed_file.parent)
        seed_data = {
            "api_slug": api_slug,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dataset": dataset,
        }
        seed_file.write_text(
            json.dumps(seed_data, indent=2) + "\n"
        )
        
        # Also create a data loader script for standalone runtime
        loader_file = dest / "load_generated_data.py"
        loader_content = f'''"""Load generated seed data into runtime storage.

This script loads the generated data from data/seeds/generated.json into
the runtime storage so it's available when the API starts.
"""

import json
from pathlib import Path

# Import runtime (will work when run from generated_output/{api_slug}/)
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    import runtime
    
    seed_file = Path(__file__).parent / "data" / "seeds" / "generated.json"
    if seed_file.exists():
        with open(seed_file) as f:
            seed_data = json.load(f)
        
        dataset = seed_data.get("dataset", {{}})
        
        # Load into runtime storage
        for component_name, records in dataset.items():
            for record in records:
                runtime.insert_component_record("{api_slug}", component_name, record)
        
        total_records = sum(len(records) for records in dataset.values())
        print(f"Loaded {{total_records}} records into runtime storage")
    else:
        print(f"Seed file not found: {{seed_file}}")
except Exception as e:
    print(f"Warning: Could not load seed data: {{e}}")
'''
        loader_file.write_text(loader_content, encoding="utf-8")
    except Exception as e:
        # Don't fail if data generation fails, just log
        print(f"Warning: Could not generate data for {api_slug}: {e}")
    
    return dest


def remove_generated_package(api_slug: str) -> None:
    dest = packages_root() / api_slug
    if dest.exists():
        shutil.rmtree(dest)
        _update_package_index()
    
    # Also remove standalone API
    output_root = Path(__file__).resolve().parent.parent.parent / "generated_output"
    standalone_dest = output_root / api_slug
    if standalone_dest.exists():
        shutil.rmtree(standalone_dest)


def _ensure_package(path: Path) -> None:
    ensure_dir(path)
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")


def _update_package_index() -> None:
    root = packages_root()
    slugs = list_packages()
    init_file = root / "__init__.py"
    content_lines = [
        '"""Versioned packages for reverse-generated APIs."""',
        "",
        "__all__ = [",
    ]
    for slug in slugs:
        content_lines.append(f'    "{slug}",')
    content_lines.append("]")
    content_lines.append("")
    init_file.write_text("\n".join(content_lines), encoding="utf-8")


def _ensure_standalone_files(dest: Path, api_slug: str) -> None:
    """
    Ensure standalone API files exist (main.py, runtime.py, requirements.txt).
    
    Creates these files if they don't exist. This allows customization - if you
    modify main.py or runtime.py, they won't be overwritten on subsequent generations.
    
    Args:
        dest: Destination directory (generated_output/{api_slug}/)
        api_slug: API slug identifier (e.g., "stripe")
    
    Raises:
        OSError: If files cannot be written
    """
    import sys
    
    # Ensure destination directory exists
    ensure_dir(dest)
    
    # main.py
    main_file = dest / "main.py"
    if not main_file.exists():
        print(f"[_ensure_standalone_files] Creating main.py at {main_file}", file=sys.stderr)
        main_content = f'''"""Standalone FastAPI application for {api_slug.title()} API mock."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from code.routes import router

app = FastAPI(
    title="{api_slug.title()} API Mock",
    description="Generated mock API for {api_slug.title()}",
    version="1.0.0",
)

# CORS: allow all origins for a standalone mock API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the generated routes
app.include_router(router)

# Load generated seed data on startup
@app.on_event("startup")
async def load_seed_data() -> None:
    """Load generated seed data into runtime storage."""
    try:
        import json
        from pathlib import Path
        
        seed_file = Path(__file__).parent / "data" / "seeds" / "generated.json"
        if seed_file.exists():
            with open(seed_file) as f:
                seed_data = json.load(f)
            
            dataset = seed_data.get("dataset", {{}})
            
            # Import runtime
            import runtime
            
            # Load into runtime storage
            for component_name, records in dataset.items():
                for record in records:
                    runtime.insert_component_record("{api_slug}", component_name, record)
            
            # Distribute account-scoped components (like balance) to each mock account
            # Get all mock account IDs from auth module if it exists
            account_scoped_components = ["balance", "balance_transaction"]
            mock_accounts = []
            
            try:
                # Try to get mock accounts from auth module (if it exists)
                from auth import _MOCK_API_KEYS
                mock_accounts = [
                    info.get("account_id") 
                    for info in _MOCK_API_KEYS.values() 
                    if info.get("account_id")
                ]
            except (ImportError, AttributeError, KeyError):
                # Auth module doesn't exist or doesn't have expected structure - use default accounts
                mock_accounts = ["acct_default", "acct_123456", "acct_production"]
            
            # Distribute account-scoped data to each account
            # Give each account at least one record (round-robin if multiple records exist)
            for component_name in account_scoped_components:
                if component_name in dataset:
                    component_records = dataset[component_name]
                    for idx, account_id in enumerate(mock_accounts):
                        if component_records:
                            record_index = idx % len(component_records)
                            record = component_records[record_index].copy()
                            runtime.insert_account_component_record(
                                account_id, component_name, record
                            )
            
            total_records = sum(len(records) for records in dataset.values())
            account_records = sum(
                len(records) 
                for component in account_scoped_components 
                if component in dataset 
                for records in [dataset[component]] 
                for _ in mock_accounts
            )
            print(f"Loaded {{total_records}} records into runtime storage")
            if account_records > 0:
                print(f"Distributed {{account_records}} account-scoped records to {{len(mock_accounts)}} accounts")
    except Exception as e:
        print(f"Warning: Could not load seed data: {{e}}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {{"status": "ok", "service": "{api_slug}-api-mock"}}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
'''
        main_file.write_text(main_content, encoding="utf-8")
        print(f"[_ensure_standalone_files] Created main.py", file=sys.stderr)
    else:
        print(f"[_ensure_standalone_files] main.py already exists, skipping", file=sys.stderr)
    
    # runtime.py - only create if missing (may have been customized)
    runtime_file = dest / "runtime.py"
    if not runtime_file.exists():
        print(f"[_ensure_standalone_files] Creating runtime.py at {runtime_file}", file=sys.stderr)
        runtime_content = '''"""Standalone in-memory runtime for the API mock."""

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
    """Insert or update a record."""
    record = dict(payload)
    key = _derive_record_key(record)
    record.setdefault("id", key)
    
    if component_name not in _storage:
        _storage[component_name] = []
    
    records = _storage[component_name]
    for i, existing_record in enumerate(records):
        existing_key = existing_record.get("id") or _derive_record_key(existing_record)
        if existing_key == key:
            records[i] = record
            return record.copy()
    
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
    """Derive a key from a payload."""
    for candidate in ("id", "uuid", "uid", "key"):
        value = payload.get(candidate)
        if value is not None:
            return str(value)
    return str(uuid4())
'''
        runtime_file.write_text(runtime_content, encoding="utf-8")
        print(f"[_ensure_standalone_files] Created runtime.py", file=sys.stderr)
    else:
        print(f"[_ensure_standalone_files] runtime.py already exists, skipping", file=sys.stderr)
    
    # requirements.txt
    req_file = dest / "requirements.txt"
    if not req_file.exists():
        print(f"[_ensure_standalone_files] Creating requirements.txt at {req_file}", file=sys.stderr)
        req_file.write_text("fastapi>=0.115.0,<1.0.0\nuvicorn[standard]>=0.30.0,<1.0.0\n", encoding="utf-8")
        print(f"[_ensure_standalone_files] Created requirements.txt", file=sys.stderr)
    else:
        print(f"[_ensure_standalone_files] requirements.txt already exists, skipping", file=sys.stderr)
