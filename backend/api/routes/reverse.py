"""FastAPI router for reverse generation workflows."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse

from ..schemas.reverse import (
    GenerateDataRequest,
    GenerateDataResponse,
    ReverseApplyRequest,
    ReverseApplyResponse,
    ReverseCleanupRequest,
    ReverseCleanupResponse,
    ReverseGenerateRequest,
    ReverseIngestRequest,
    ReverseIngestResponse,
    ReversePlanRequest,
)
from reverse import (
    data_synthesizer,
    generator,
    package_manager,
    planner,
    preview,
    runtime,
    spec_loader,
    validator,
)
from reverse.models import GenerationReport, PreviewResponse
from reverse.storage import remove_generated_folder

router = APIRouter(prefix="/reverse", tags=["reverse"])


@router.post("/ingest_spec", response_model=ReverseIngestResponse)
def reverse_ingest_spec(payload: ReverseIngestRequest) -> ReverseIngestResponse:
    try:
        result = spec_loader.ingest_spec(payload.spec, explicit_name=payload.api_name)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReverseIngestResponse(
        api_slug=result.api_slug,
        api_name=result.api_name,
        version=result.version,
        route_count=len(result.route_inventory),
        route_inventory=result.route_inventory,
    )


@router.post("/plan", response_class=PlainTextResponse)
def reverse_plan_endpoint(payload: ReversePlanRequest) -> PlainTextResponse:
    try:
        plan = planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    validator.validate_plan(plan)
    markdown = planner.render_plan_markdown(plan)
    return PlainTextResponse(content=markdown, media_type="text/markdown")


@router.post("/generate", response_model=GenerationReport)
def reverse_generate_endpoint(payload: ReverseGenerateRequest) -> GenerationReport:
    try:
        plan = planner.build_plan(payload.api_slug)
    except FileNotFoundError:
        plan = None
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if plan:
        validator.validate_plan(plan)

    try:
        report = generator.generate(plan, payload.api_slug)
        
        # Automatically generate data for ALL components after code generation
        # This uses graph-based generation to create data for every component
        try:
            dataset = data_synthesizer.synthesize_all_components(
                payload.api_slug,
                count_per_component=None,  # Uses default of 3 per component
                store_in_db=False,  # We'll use replace_dataset to store all at once
            )
            
            # Store all generated records in GeneratedRecord database table
            if dataset:
                runtime.replace_dataset(payload.api_slug, dataset)
        except Exception as e:
            # Don't fail code generation if data generation fails
            # Just log it (could add proper logging here)
            print(f"Warning: Data generation failed for {payload.api_slug}: {e}")
        
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return report


@router.get("/preview", response_model=PreviewResponse)
def reverse_preview_endpoint(api_slug: str) -> PreviewResponse:
    return preview.preview(api_slug)


@router.post("/apply", response_model=ReverseApplyResponse)
def reverse_apply_endpoint(payload: ReverseApplyRequest, request: Request) -> ReverseApplyResponse:
    try:
        plan = planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    validator.validate_plan(plan)

    # Generate code
    report = generator.generate(plan, payload.api_slug)
    
    # Generate data for ALL components using dependency graph
    # This uses graph-based generation to create data for every component
    # store_adb=False because we'll use replace_dataset to store everything at once
    dataset = data_synthesizer.synthesize_all_components(
        payload.api_slug,
        count_per_component=None,  # Uses default of 3 per component
        store_in_db=False,  # We'll use replace_dataset to store all at once
    )
    
    # Store all generated records in GeneratedRecord database table
    if dataset:
        runtime.replace_dataset(payload.api_slug, dataset)
    
    # Sync to generated_apis (for import in main backend)
    package_path = package_manager.sync_generated_package(payload.api_slug)
    
    # Sync to generated_output (standalone API with main.py, runtime.py, etc.)
    standalone_path = package_manager.sync_standalone_api(payload.api_slug)
    
    # Mount routes in main backend
    runtime.mount_generated_routes(request.app, payload.api_slug, prefix=f"/generated/{payload.api_slug}")

    return ReverseApplyResponse(
        applied=True,
        message=(
            f"Generated assets for '{payload.api_slug}' applied. "
            f"Routes available under /generated/{payload.api_slug}. "
            f"Package synced to {package_path}. "
            f"Standalone API synced to {standalone_path}."
        ),
    )


@router.post("/cleanup", response_model=ReverseCleanupResponse)
def reverse_cleanup_endpoint(payload: ReverseCleanupRequest) -> ReverseCleanupResponse:
    runtime.remove_dataset(payload.api_slug)
    package_manager.remove_generated_package(payload.api_slug)
    remove_generated_folder(payload.api_slug)
    return ReverseCleanupResponse(removed=True)


@router.post("/generate_data", response_model=GenerateDataResponse)
def reverse_generate_data(payload: GenerateDataRequest) -> GenerateDataResponse:
    try:
        plan = planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if payload.use_graph:
        # Generate data for ALL components using dependency graph
        # OpenAI API key is read from OPENAI_API_KEY environment variable
        dataset = data_synthesizer.synthesize_all_components(
            payload.api_slug,
            payload.counts,
            seed_account_id=payload.seed_account_id,
        )
    else:
        # Original route-based generation
        dataset = data_synthesizer.synthesize(plan, payload.counts, payload.seed)
    
    return GenerateDataResponse(
        api_slug=payload.api_slug,
        generated_at=datetime.now(timezone.utc),
        dataset=dataset,
    )
