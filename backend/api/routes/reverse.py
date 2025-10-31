"""FastAPI router for reverse generation workflows."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request

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
from reverse.models import GenerationReport, PreviewResponse, ReversePlan
from reverse.storage import api_root, remove_generated_folder, write_json

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


@router.post("/plan", response_model=ReversePlan)
def reverse_plan_endpoint(payload: ReversePlanRequest) -> ReversePlan:
    try:
        plan = planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    validator.validate_plan(plan)
    write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())
    return plan


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
        write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())

    try:
        report = generator.generate(plan, payload.api_slug)
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
    write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())

    report = generator.generate(plan, payload.api_slug)
    dataset = data_synthesizer.synthesize(plan)
    runtime.replace_dataset(payload.api_slug, dataset)
    package_path = package_manager.sync_generated_package(payload.api_slug)
    runtime.mount_generated_routes(request.app, payload.api_slug, prefix=f"/generated/{payload.api_slug}")

    return ReverseApplyResponse(
        applied=True,
        message=(
            f"Generated assets for '{payload.api_slug}' applied. "
            f"Routes available under /generated/{payload.api_slug}. "
            f"Package synced to {package_path}."
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

    dataset = data_synthesizer.synthesize(plan, payload.counts, payload.seed)
    return GenerateDataResponse(
        api_slug=payload.api_slug,
        generated_at=datetime.now(timezone.utc),
        dataset=dataset,
    )
