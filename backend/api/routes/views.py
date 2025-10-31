"""FastAPI router for server-rendered HTML views."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ingestion import (
    get_component_entry,
    get_component_properties,
    list_apis as fetch_api_registry,
    list_components as fetch_component_registry,
)

router = APIRouter(tags=["views"])

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[2] / "templates"))


@router.get("/", response_class=HTMLResponse)
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


@router.get(
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
