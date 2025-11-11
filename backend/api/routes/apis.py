"""FastAPI router for ingestion and component-centric endpoints."""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..schemas.apis import (
    ApiSummary,
    ComponentDetail,
    ComponentGraph,
    ComponentMeta,
    ComponentResponse,
    IngestionResponse,
    PropertyRow,
)
from ingestion import (
    IngestionResult,
    construct_component_graph,
    get_component_entry,
    get_component_properties,
    ingest_openapi_spec,
    list_apis as fetch_api_registry,
    list_components as fetch_component_registry,
)
from reverse.models import RouteInventoryEntry
from reverse.planner import build_plan, load_route_inventory
from reverse.spec_loader import ingest_spec as reverse_ingest_spec
from reverse import (
    data_synthesizer,
    generator,
    package_manager,
    runtime,
    validator,
)

router = APIRouter(prefix="/apis", tags=["apis"])


@router.post("/upload", response_model=IngestionResponse)
async def upload_openapi_spec(
    spec_file: UploadFile = File(...),
    api_name: Optional[str] = Form(None),
) -> IngestionResponse:
    try:
        raw_bytes = await spec_file.read()
    finally:
        await spec_file.close()

    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="OpenAPI spec must be UTF-8 encoded.") from exc

    try:
        result: IngestionResult = ingest_openapi_spec(raw_text, explicit_name=api_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    try:
        reverse_ingest_spec(raw_text, explicit_name=result.api_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Failed to stage routes: {exc}") from exc
    except (RuntimeError, TypeError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to stage routes: {exc}") from exc

    # Automatically generate and apply API after upload
    try:
        plan = build_plan(result.api_slug)
        validator.validate_plan(plan)
        
        # Generate code
        generator.generate(plan, result.api_slug)
        
        # Generate data for ALL components using dependency graph
        dataset = None
        try:
            dataset = data_synthesizer.synthesize_all_components(
                result.api_slug,
                count_per_component=None,  # Uses default of 3 per component
                store_in_db=False,  # We'll use replace_dataset to store all at once
            )
            
            # Store all generated records in GeneratedRecord database table
            if dataset:
                runtime.replace_dataset(result.api_slug, dataset)
        except Exception as e:
            # Don't fail if data generation fails
            print(f"Warning: Data generation failed for {result.api_slug}: {e}")
        
        # Sync to generated_apis (for import in main backend)
        package_manager.sync_generated_package(result.api_slug)
        
        # Sync to generated_output (standalone API with main.py, runtime.py, etc.)
        package_manager.sync_standalone_api(result.api_slug)
        
        # Priority 2: Create initial state when API is generated
        try:
            from rl.state_manager import StateManager
            state_manager = StateManager()
            initial_state_id = state_manager.get_initial_state(
                result.api_slug, 
                seed_data=dataset if dataset else None
            )
            print(f"[upload] Created initial state {initial_state_id} for {result.api_slug}")
        except Exception as e:
            # Don't fail upload if RL state creation fails
            print(f"Warning: Failed to create initial RL state for {result.api_slug}: {e}")
        
        # Note: Routes are auto-mounted on server startup, so no need to mount here
        print(f"[upload] Successfully generated and applied API: {result.api_slug}")
    except Exception as exc:
        # Log but don't fail the upload if generation fails
        # The API can be generated later via /reverse/generate and /reverse/apply endpoints
        print(f"Warning: Auto-generation failed for {result.api_slug}: {exc}")
        import traceback
        traceback.print_exc()

    return IngestionResponse(
        api_slug=result.api_slug,
        api_name=result.api_name,
        version=result.version,
        components=[
            ComponentResponse(
                component_name=component.component_name,
                storage_key=component.storage_key,
                property_count=component.property_count,
            )
            for component in result.components
        ],
    )


@router.get("", response_model=list[ApiSummary])
def list_apis_endpoint() -> list[ApiSummary]:
    try:
        apis = fetch_api_registry()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return [ApiSummary(**api) for api in apis]


@router.get("/{api_slug}/components", response_model=list[ComponentMeta])
def list_components_endpoint(api_slug: str) -> list[ComponentMeta]:
    try:
        components = fetch_component_registry(api_slug)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return [ComponentMeta(**component) for component in components]


@router.get("/{api_slug}/components/{component_name}", response_model=ComponentDetail)
def get_component_details(api_slug: str, component_name: str) -> ComponentDetail:
    try:
        entry = get_component_entry(api_slug, component_name)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if not entry:
        raise HTTPException(status_code=404, detail="Component not found.")

    properties = get_component_properties(entry)
    schema: Dict[str, Any] = entry.get("schema") or {}
    return ComponentDetail(
        component_name=component_name,
        storage_key=entry.get("storage_key"),
        component_schema=schema,
        properties=[PropertyRow(**row) for row in properties],
    )


@router.get("/{api_slug}/graph", response_model=ComponentGraph)
def get_component_graph(api_slug: str) -> ComponentGraph:
    try:
        graph = construct_component_graph(api_slug)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ComponentGraph(**graph)


@router.get("/{api_slug}/routes", response_model=list[RouteInventoryEntry])
def list_routes(api_slug: str) -> list[RouteInventoryEntry]:
    try:
        return load_route_inventory(api_slug)
    except FileNotFoundError:
        return []
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
