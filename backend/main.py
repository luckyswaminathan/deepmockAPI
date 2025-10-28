from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import init_core_tables
from ingestion import (
    IngestionResult,
    get_component_entry,
    get_component_properties,
    construct_component_graph,
    ingest_openapi_spec,
    list_apis as fetch_api_registry,
    list_components as fetch_component_registry,
)
from reverse import (
    data_synthesizer as reverse_data_synthesizer,
    generator as reverse_generator,
    runtime as reverse_runtime,
    package_manager as reverse_package_manager,
    planner as reverse_planner,
    preview as reverse_preview,
    spec_loader as reverse_spec_loader,
    validator as reverse_validator,
)
from reverse.models import (
    GenerationReport,
    PreviewResponse,
    ReversePlan,
    RouteInventoryEntry,
)
from reverse.storage import remove_generated_folder, write_json, api_root
from reverse.planner import load_route_inventory

app = FastAPI(title="DeepMock API Backend")

# CORS: allow local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class ComponentResponse(BaseModel):
    component_name: str
    storage_key: str
    property_count: int


class IngestionResponse(BaseModel):
    api_slug: str
    api_name: str
    version: Optional[str]
    components: list[ComponentResponse]


class ApiSummary(BaseModel):
    api_slug: str
    api_name: str
    title: str
    version: Optional[str] = None
    created_at: datetime


class ComponentMeta(BaseModel):
    component_name: str
    storage_key: str
    property_count: int
    created_at: datetime


class PropertyRow(BaseModel):
    position: Optional[int] = None
    property_name: str
    property_type: Optional[str] = None
    property_format: Optional[str] = None
    is_required: bool
    description: Optional[str] = None
    example: Optional[Any] = None
    reference: Optional[str] = None


class ComponentDetail(BaseModel):
    component_name: str
    storage_key: Optional[str] = None
    component_schema: Dict[str, Any]
    properties: list[PropertyRow]


class ComponentGraphNode(BaseModel):
    component_name: str
    storage_key: str
    created_at: datetime
    property_count: int
    references: list[str]
    dependent_count: int


class ComponentGraphEdge(BaseModel):
    source: str
    target: str


class ComponentGraph(BaseModel):
    nodes: list[ComponentGraphNode]
    edges: list[ComponentGraphEdge]


class ReverseIngestRequest(BaseModel):
    spec: Dict[str, Any]
    api_name: Optional[str] = None


class ReverseIngestResponse(BaseModel):
    api_slug: str
    api_name: str
    version: Optional[str]
    route_count: int
    route_inventory: list[RouteInventoryEntry]


class ReversePlanRequest(BaseModel):
    api_slug: str


class ReverseGenerateRequest(BaseModel):
    api_slug: str


class ReverseApplyRequest(BaseModel):
    api_slug: str
    paths: Optional[list[str]] = None


class ReverseApplyResponse(BaseModel):
    applied: bool
    message: str


class ReverseCleanupRequest(BaseModel):
    api_slug: str


class ReverseCleanupResponse(BaseModel):
    removed: bool


class GenerateDataRequest(BaseModel):
    api_slug: str
    counts: Optional[Dict[str, int]] = None
    seed: int = 1337


class GenerateDataResponse(BaseModel):
    api_slug: str
    generated_at: datetime
    dataset: Dict[str, list[Dict[str, Any]]]


@app.on_event("startup")
def on_startup() -> None:
    try:
        init_core_tables()
    except RuntimeError as exc:
        raise RuntimeError(
            "Failed to initialize database connection. "
            "Ensure DATABASE_URL is set to a valid PostgreSQL connection string."
        ) from exc


@app.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/apis/upload", response_model=IngestionResponse)
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
        reverse_spec_loader.ingest_spec(raw_text, explicit_name=result.api_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Failed to stage routes: {exc}") from exc
    except (RuntimeError, TypeError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to stage routes: {exc}") from exc

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


@app.get("/apis", response_model=list[ApiSummary])
def list_apis_endpoint() -> list[ApiSummary]:
    try:
        apis = fetch_api_registry()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return [ApiSummary(**api) for api in apis]


@app.get("/apis/{api_slug}/components", response_model=list[ComponentMeta])
def list_components_endpoint(api_slug: str) -> list[ComponentMeta]:
    try:
        components = fetch_component_registry(api_slug)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return [ComponentMeta(**component) for component in components]


@app.get("/apis/{api_slug}/components/{component_name}", response_model=ComponentDetail)
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


@app.get("/apis/{api_slug}/graph", response_model=ComponentGraph)
def get_component_graph(api_slug: str) -> ComponentGraph:
    try:
        graph = construct_component_graph(api_slug)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ComponentGraph(**graph)


@app.get("/apis/{api_slug}/routes", response_model=list[RouteInventoryEntry])
def list_routes(api_slug: str) -> list[RouteInventoryEntry]:
    try:
        routes = load_route_inventory(api_slug)
    except FileNotFoundError:
        return []
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return routes


@app.post("/reverse/ingest_spec", response_model=ReverseIngestResponse)
def reverse_ingest_spec(payload: ReverseIngestRequest) -> ReverseIngestResponse:
    try:
        result = reverse_spec_loader.ingest_spec(payload.spec, explicit_name=payload.api_name)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReverseIngestResponse(
        api_slug=result.api_slug,
        api_name=result.api_name,
        version=result.version,
        route_count=len(result.route_inventory),
        route_inventory=result.route_inventory,
    )


@app.post("/reverse/plan", response_model=ReversePlan)
def reverse_plan_endpoint(payload: ReversePlanRequest) -> ReversePlan:
    try:
        plan = reverse_planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    reverse_validator.validate_plan(plan)
    write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())
    return plan


@app.post("/reverse/generate", response_model=GenerationReport)
def reverse_generate_endpoint(payload: ReverseGenerateRequest) -> GenerationReport:
    try:
        plan = reverse_planner.build_plan(payload.api_slug)
    except FileNotFoundError:
        plan = None
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if plan:
        reverse_validator.validate_plan(plan)
        write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())

    try:
        report = reverse_generator.generate(plan, payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return report


@app.get("/reverse/preview", response_model=PreviewResponse)
def reverse_preview_endpoint(api_slug: str) -> PreviewResponse:
    return reverse_preview.preview(api_slug)


@app.post("/reverse/apply", response_model=ReverseApplyResponse)
def reverse_apply_endpoint(payload: ReverseApplyRequest) -> ReverseApplyResponse:
    try:
        plan = reverse_planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    reverse_validator.validate_plan(plan)
    write_json(api_root(payload.api_slug) / "plan" / "plan.json", plan.dict())

    report = reverse_generator.generate(plan, payload.api_slug)
    dataset = reverse_data_synthesizer.synthesize(plan)
    reverse_runtime.replace_dataset(payload.api_slug, dataset)
    package_path = reverse_package_manager.sync_generated_package(payload.api_slug)
    reverse_runtime.mount_generated_routes(app, payload.api_slug, prefix=f"/generated/{payload.api_slug}")

    return ReverseApplyResponse(
        applied=True,
        message=(
            f"Generated assets for '{payload.api_slug}' applied. "
            f"Routes available under /generated/{payload.api_slug}. "
            f"Package synced to {package_path}."
        ),
    )


@app.post("/reverse/cleanup", response_model=ReverseCleanupResponse)
def reverse_cleanup_endpoint(payload: ReverseCleanupRequest) -> ReverseCleanupResponse:
    reverse_runtime.remove_dataset(payload.api_slug)
    reverse_package_manager.remove_generated_package(payload.api_slug)
    remove_generated_folder(payload.api_slug)
    return ReverseCleanupResponse(removed=True)


@app.post("/reverse/generate_data", response_model=GenerateDataResponse)
def reverse_generate_data(payload: GenerateDataRequest) -> GenerateDataResponse:
    try:
        plan = reverse_planner.build_plan(payload.api_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    dataset = reverse_data_synthesizer.synthesize(plan, payload.counts, payload.seed)
    return GenerateDataResponse(
        api_slug=payload.api_slug,
        generated_at=datetime.now(timezone.utc),
        dataset=dataset,
    )


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    error: Optional[str] = None
    try:
        apis = fetch_api_registry()
    except RuntimeError as exc:
        apis = []
        error = str(exc)

    api_components: Dict[str, list[Dict[str, Any]]] = {}
    for api in apis:
        try:
            api_components[api["api_slug"]] = fetch_component_registry(api["api_slug"])
        except RuntimeError as exc:  # pragma: no cover - defensive logging
            api_components[api["api_slug"]] = []
            error = str(exc)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "apis": apis,
            "api_components": api_components,
            "error": error,
        },
    )


@app.get(
    "/apis/{api_slug}/components/{component_name}/view",
    response_class=HTMLResponse,
)
def view_component_page(request: Request, api_slug: str, component_name: str) -> HTMLResponse:
    try:
        entry = get_component_entry(api_slug, component_name)
    except RuntimeError as exc:
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    if not entry:
        raise HTTPException(status_code=404, detail="Component not found.")

    rows = get_component_properties(entry)

    return templates.TemplateResponse(
        "component.html",
        {
            "request": request,
            "api_slug": api_slug,
            "component_name": component_name,
            "storage_key": entry.get("storage_key"),
            "component_schema": entry.get("schema") or {},
            "rows": rows,
        },
    )


if __name__ == "__main__":
    # Enable local development with: python backend/main.py
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
