from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
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
from reverse.storage import api_root, read_json, write_json, write_text
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


def _extract_component_name_from_ref(ref: str) -> Optional[str]:
    """Extract component name from OpenAPI schema reference like '#/components/schemas/User'."""
    if not ref or not isinstance(ref, str):
        return None
    # Handle format: #/components/schemas/ComponentName
    if ref.startswith("#/components/schemas/"):
        return ref.split("/")[-1]
    # Handle format: components/schemas/ComponentName
    if "/schemas/" in ref:
        return ref.split("/schemas/")[-1].split("/")[0]
    return None


def _infer_base_component_name(ref_name: str, component_names: list[str]) -> Optional[str]:
    """Try to infer base component name from request/response types like 'CreateUserRequest' -> 'User'."""
    ref_lower = ref_name.lower()
    component_lower_map = {name.lower(): name for name in component_names}
    
    # Remove common prefixes/suffixes and try to match
    prefixes_to_remove = ["create", "update", "patch", "delete", "get", "post", "put"]
    suffixes_to_remove = ["request", "response", "dto", "model", "body", "payload"]
    
    # Try exact match first
    if ref_lower in component_lower_map:
        return component_lower_map[ref_lower]
    
    # Try removing common prefixes
    for prefix in prefixes_to_remove:
        if ref_lower.startswith(prefix):
            candidate = ref_name[len(prefix):]
            candidate_lower = candidate.lower()
            if candidate_lower in component_lower_map:
                return component_lower_map[candidate_lower]
    
    # Try removing common suffixes
    for suffix in suffixes_to_remove:
        if ref_lower.endswith(suffix):
            candidate = ref_name[:-len(suffix)]
            candidate_lower = candidate.lower()
            if candidate_lower in component_lower_map:
                return component_lower_map[candidate_lower]
    
    # Try partial match (component name contained in ref name)
    for component_lower, component_name in component_lower_map.items():
        if component_lower in ref_lower and len(component_lower) >= 3:
            return component_name
    
    return None


def _resolve_component_from_refs(
    route: RouteInventoryEntry,
    component_names: list[str],
    method: str,
) -> Optional[str]:
    """Resolve component name from explicit schema references, with fallback logic."""
    # For GET requests, prioritize response body ref
    # For POST/PUT/PATCH, prioritize request body ref
    # For DELETE, try both
    refs_to_check: list[Optional[str]] = []
    
    if method == "GET":
        refs_to_check = [route.response_body_ref]
    elif method in {"POST", "PUT", "PATCH"}:
        refs_to_check = [route.request_body_ref, route.response_body_ref]
    else:  # DELETE or other methods
        refs_to_check = [route.request_body_ref, route.response_body_ref]
    
    # Try explicit refs first
    for ref in refs_to_check:
        if not ref:
            continue
        
        ref_component_name = _extract_component_name_from_ref(ref)
        if not ref_component_name:
            continue
        
        # Check if exact match exists
        if ref_component_name in component_names:
            return ref_component_name
        
        # Try to infer base component from request/response types
        inferred = _infer_base_component_name(ref_component_name, component_names)
        if inferred:
            return inferred
    
    return None


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

        ## TODO: need to have better operation Mapping - use some form of GPT labelling, etc
        ## plug in API label (so essentially our operations also are robust)
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

        # Try to resolve component from explicit schema references first
        component = _resolve_component_from_refs(route, component_names, method)
        
        print(component)
        # Fall back to path-based guessing if no explicit refs found
        if component is None:
            component = guess_component_from_path(route.path, component_names)
        
        warnings: list[str] = []
        if component is None:
            warnings.append("Unable to determine component from route path or schema references.")
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
    plan_dir = api_root(api_slug) / "plan"
    write_json(plan_dir / "plan.json", plan.dict())
    write_text(plan_dir / "plan.md", render_plan_markdown(plan))
    
    # Generate component-specific plan files for agentic generation
    _write_component_plans(plan_dir, plan)
    
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


OPERATION_DESCRIPTIONS = {
    "create": "Create a new record for the component.",
    "read_one": "Fetch a single record by identifier.",
    "read_many": "List or search records.",
    "update": "Replace a full record.",
    "update_partial": "Apply a partial update to a record.",
    "delete": "Remove a record.",
}

OPERATION_ORDER = ["create", "read_one", "read_many", "update", "update_partial", "delete"]


def render_plan_markdown(plan: ReversePlan) -> str:
    """Render a concise summary plan suitable for agentic generation."""
    lines: list[str] = []
    lines.append(f"# Reverse Engineering Plan for `{plan.api_slug}`")
    lines.append("")
    lines.append(f"**Total Routes:** {len(plan.routes)}")
    lines.append(f"**Generated At:** {plan.generated_at.isoformat()}")
    lines.append("")
    
    lines.append("## Agent Directives")
    lines.append("1. Review the component summary below to understand the CRUD surface.")
    lines.append("2. Use component-specific plans in `plan/components/` for detailed route information.")
    lines.append("3. Implement server handlers that satisfy the described operations and filters.")
    lines.append("4. Raise any ambiguities called out in validation warnings before coding.")
    lines.append("")

    if plan.validation.errors or plan.validation.warnings:
        lines.append("## Validation Summary")
        if plan.validation.errors:
            lines.append("### Errors")
            for entry in plan.validation.errors[:10]:  # Limit to first 10
                lines.append(f"- ⚠️ {entry}")
            if len(plan.validation.errors) > 10:
                lines.append(f"- ... and {len(plan.validation.errors) - 10} more errors")
        if plan.validation.warnings:
            lines.append("### Warnings")
            for entry in plan.validation.warnings[:10]:  # Limit to first 10
                lines.append(f"- ⚠️ {entry}")
            if len(plan.validation.warnings) > 10:
                lines.append(f"- ... and {len(plan.validation.warnings) - 10} more warnings")
        lines.append("")

    # Group routes by component
    component_routes: dict[str | None, list[RoutePlan]] = defaultdict(list)
    component_operations: dict[str, set[str]] = defaultdict(set)
    
    for route in plan.routes:
        component_routes[route.component].append(route)
        for operation in route.operations:
            if operation.component:
                component_operations[operation.component].add(operation.type)

    lines.append("## Component Summary")
    lines.append("")
    lines.append("Each component below has a dedicated plan file in `plan/components/` with detailed route information.")
    lines.append("")
    
    if component_operations:
        lines.append("| Component | Operations | Route Count | Plan File |")
        lines.append("|-----------|------------|-------------|-----------|")
        
        for component in sorted(component_operations.keys()):
            ordered_ops = [op for op in OPERATION_ORDER if op in component_operations[component]]
            ops_str = ", ".join([f"`{op}`" for op in ordered_ops]) if ordered_ops else "None"
            route_count = len(component_routes.get(component, []))
            plan_file = f"`plan/components/{component.lower().replace('.', '_')}.md`"
            lines.append(f"| `{component}` | {ops_str} | {route_count} | {plan_file} |")
    else:
        lines.append("- No component operations could be inferred from the plan.")
    
    lines.append("")
    lines.append("## Quick Stats")
    lines.append("")
    
    # Count operations by type
    operation_counts: dict[str, int] = defaultdict(int)
    for route in plan.routes:
        for operation in route.operations:
            operation_counts[operation.type] += 1
    
    lines.append("**Operations by Type:**")
    for op_type in OPERATION_ORDER:
        if op_type in operation_counts:
            lines.append(f"- `{op_type}`: {operation_counts[op_type]} routes")
    
    lines.append("")
    lines.append("**Routes by Status:**")
    status_counts: dict[str, int] = defaultdict(int)
    for route in plan.routes:
        status_counts[route.status] += 1
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count} routes")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Note:** For detailed route-by-route information, see individual component plan files in `plan/components/`.")
    lines.append("")

    return "\n".join(lines)


def _write_component_plans(plan_dir: Path, plan: ReversePlan) -> None:
    """Generate component-specific plan files for better agentic processing."""
    # Group routes by component
    component_routes: dict[str | None, list[RoutePlan]] = defaultdict(list)
    for route in plan.routes:
        component_routes[route.component].append(route)
    
    components_dir = plan_dir / "components"
    components_dir.mkdir(exist_ok=True)
    
    # Generate a plan file for each component
    for component, routes in component_routes.items():
        if component is None:
            continue  # Skip unmapped routes for now
        
        # Sanitize component name for filename
        safe_name = component.lower().replace(".", "_").replace("/", "_")
        component_plan_path = components_dir / f"{safe_name}.md"
        
        content = _render_component_plan(component, routes, plan)
        write_text(component_plan_path, content)
    
    # Also create a plan for unmapped routes if any
    if None in component_routes:
        unmapped_plan_path = components_dir / "unmapped.md"
        content = _render_component_plan("Unmapped Routes", component_routes[None], plan)
        write_text(unmapped_plan_path, content)


def _render_component_plan(component_name: str, routes: list[RoutePlan], plan: ReversePlan) -> str:
    """Render detailed plan for a specific component."""
    lines: list[str] = []
    lines.append(f"# Component Plan: `{component_name}`")
    lines.append("")
    lines.append(f"**API Slug:** `{plan.api_slug}`")
    lines.append(f"**Total Routes:** {len(routes)}")
    lines.append("")
    
    # Get unique operations for this component
    operations_set: set[str] = set()
    for route in routes:
        for operation in route.operations:
            print(operation)
            if operation.component == component_name or (component_name == "Unmapped Routes" and not operation.component):
                operations_set.add(operation.type)
    
    if operations_set:
        lines.append("## Supported Operations")
        ordered_ops = [op for op in OPERATION_ORDER if op in operations_set]
        for op in ordered_ops:
            print(op)
            description = OPERATION_DESCRIPTIONS.get(op, op)
            lines.append(f"- **`{op}`**: {description}")
        lines.append("")
    
    lines.append("## Routes")
    lines.append("")
    
    # Group routes by HTTP method for easier reading
    routes_by_method: dict[str, list[RoutePlan]] = defaultdict(list)
    for route in routes:
        routes_by_method[route.method].append(route)
    
    for method in sorted(routes_by_method.keys()):
        method_routes = routes_by_method[method]
        lines.append(f"### {method} Routes ({len(method_routes)})")
        lines.append("")
        
        for route in sorted(method_routes, key=lambda r: r.path):
            lines.append(f"#### `{route.method} {route.path}`")
            
            if route.summary:
                lines.append(f"**Summary:** {route.summary}")
            
            lines.append(f"**Status:** {route.status}")
            lines.append("")

            if route.operations:
                lines.append("**Operations:**")
                for operation in route.operations:
                    lines.append(f"- **{operation.type}**")
                    if operation.component:
                        lines.append(f"  - Component: `{operation.component}`")
                    
                    if operation.filters:
                        lines.append("  - Filters:")
                        for filt in operation.filters:
                            lines.append(f"    - `{filt.field}` {filt.operator} `{filt.value_source}`")
                    
                    if operation.notes:
                        lines.append("  - Notes:")
                        for note in operation.notes:
                            lines.append(f"    - {note}")
            else:
                lines.append("**Operations:** None")
            
            if route.warnings:
                lines.append("**Warnings:**")
                for warning in route.warnings:
                    lines.append(f"- {warning}")
            
            lines.append("")
    
    return "\n".join(lines)
