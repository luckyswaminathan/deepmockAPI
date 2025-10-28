from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

from ingestion import get_component_entry, get_component_properties, list_components
from reverse.models import (
    OperationFilter,
    OperationPlan,
    PlanValidation,
    ReversePlan,
    RouteInventoryEntry,
    RoutePlan,
)
from reverse.storage import api_root, read_json, write_json
from reverse.utils import extract_path_params, guess_component_from_path, normalise_method


METHOD_OPERATION_MAP = {
    "GET": "read_many",
    "POST": "create",
    "PUT": "update",
    "PATCH": "update_partial",
    "DELETE": "delete",
}


def load_route_inventory(api_slug: str) -> list[RouteInventoryEntry]:
    path = api_root(api_slug) / "plan" / "route_inventory.json"
    if not path.exists():
        raise FileNotFoundError(f"No route inventory found for API slug '{api_slug}'.")
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError("Route inventory file is malformed; expected a list.")
    routes: list[RouteInventoryEntry] = []
    for entry in payload:
        routes.append(RouteInventoryEntry.parse_obj(entry))
    return routes


def build_plan(api_slug: str, *, route_inventory: Optional[Iterable[RouteInventoryEntry]] = None) -> ReversePlan:
    if route_inventory is None:
        routes = load_route_inventory(api_slug)
    else:
        routes = list(route_inventory)

    components = list_components(api_slug)
    component_names = [component["component_name"] for component in components]

    component_fields: dict[str, list[str]] = {}
    for component in component_names:
        entry = get_component_entry(api_slug, component)
        if not entry:
            continue
        rows = get_component_properties(entry)
        fields = [row["property_name"] for row in rows if isinstance(row.get("property_name"), str)]
        component_fields[component] = fields

    validation = PlanValidation()
    planned_routes: list[RoutePlan] = []

    for route in routes:
        method = normalise_method(route.method)
        operation_type = METHOD_OPERATION_MAP.get(method)
        if not operation_type:
            validation.warnings.append(f"Route {route.method} {route.path} uses unsupported method.")
            status = "skipped"
            planned_routes.append(
                RoutePlan(
                    method=route.method,
                    path=route.path,
                    component=None,
                    summary=route.summary,
                    operations=[],
                    warnings=["Unsupported HTTP method for planning."],
                    status=status,
                )
            )
            continue

        component = guess_component_from_path(route.path, component_names)
        warnings: list[str] = []
        if component is None:
            warnings.append("Unable to determine component from route path.")
            validation.warnings.append(f"No component mapping found for {route.method} {route.path}.")

        operations: list[OperationPlan] = []
        if component:
            operations.append(
                OperationPlan(
                    type=_pick_operation_type(operation_type, route),
                    component=component,
                    filters=_build_filters(component, route, component_fields.get(component, [])),
                    joins=[],
                    notes=_build_notes(route),
                )
            )
        else:
            validation.errors.append(f"Missing component mapping for {route.method} {route.path}.")

        planned_routes.append(
            RoutePlan(
                method=route.method,
                path=route.path,
                component=component,
                summary=route.summary,
                operations=operations,
                warnings=warnings,
                status="planned" if operations else "needs_mapping",
            )
        )

    plan = ReversePlan(
        api_slug=api_slug,
        generated_at=datetime.now(timezone.utc),
        routes=planned_routes,
        validation=validation,
    )
    write_json(api_root(api_slug) / "plan" / "plan.json", plan.dict())
    return plan


def _pick_operation_type(operation_type: str, route: RouteInventoryEntry) -> str:
    if operation_type == "read_many":
        params = route.path_parameters or extract_path_params(route.path)
        if params:
            return "read_one"
    return operation_type


def _build_filters(component: str, route: RouteInventoryEntry, fields: list[str]) -> list[OperationFilter]:
    filters: list[OperationFilter] = []
    path_params = route.path_parameters or extract_path_params(route.path)
    for param in path_params:
        field = _match_field(param, fields)
        filters.append(
            OperationFilter(
                field=field or param,
                value_source=f"path.{param}",
            )
        )
    return filters


def _match_field(param: str, fields: list[str]) -> Optional[str]:
    param_lower = param.lower()
    for field in fields:
        if field.lower() == param_lower:
            return field
        if field.lower() == f"{param_lower}_id":
            return field
    for field in fields:
        if param_lower in field.lower():
            return field
    return None


def _build_notes(route: RouteInventoryEntry) -> list[str]:
    notes: list[str] = []
    if route.request_body_ref:
        notes.append(f"Request body references {route.request_body_ref}")
    if route.response_body_ref:
        notes.append(f"Response body references {route.response_body_ref}")
    if route.query_parameters:
        notes.append("Query parameters: " + ", ".join(route.query_parameters))
    return notes
