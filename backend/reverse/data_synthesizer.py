from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from ingestion import get_component_entry, get_component_properties
from reverse.models import ReversePlan, RoutePlan
from reverse.planner import build_plan, load_route_inventory


def ensure_plan(api_slug: str, plan: Optional[ReversePlan] = None) -> ReversePlan:
    return plan or build_plan(api_slug, route_inventory=load_route_inventory(api_slug))


def synthesize(
    plan: ReversePlan,
    count_by_component: Optional[Dict[str, int]] = None,
    seed: int = 1337,
) -> Dict[str, list[dict]]:
    count_by_component = count_by_component or {}
    components = {route.component for route in plan.routes if route.component}
    dataset: Dict[str, list[dict]] = {}
    for component in components:
        if not component:
            continue
        count = count_by_component.get(component, 3)
        entry = get_component_entry(plan.api_slug, component)
        properties = get_component_properties(entry) if entry else []
        fields = [row["property_name"] for row in properties if isinstance(row.get("property_name"), str)]
        dataset[component] = [_build_record(component, fields, idx, seed) for idx in range(count)]
    return dataset


def _build_record(component: str, fields: list[str], index: int, seed: int) -> dict:
    record: dict[str, Optional[str]] = {
        "_generated_at": datetime.now(timezone.utc).isoformat(),
        "_seed": seed,
        "_component": component,
        "_index": index,
    }
    for field in fields:
        record[field] = _sample_value(component, field, index)
    if "id" not in record:
        record["id"] = f"{component.lower()}_{index}"
    return record


def _sample_value(component: str, field: str, index: int) -> str:
    field_lower = field.lower()
    if field_lower in {"id", f"{component.lower()}_id"} or field_lower.endswith("id"):
        return f"{component.lower()}_{index}"
    if "name" in field_lower:
        return f"{component} {index}"
    if "status" in field_lower:
        return "generated"
    if "created" in field_lower or "updated" in field_lower:
        return datetime.now(timezone.utc).isoformat()
    return f"{field_lower}_{index}"
