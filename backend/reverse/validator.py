from __future__ import annotations

from typing import Iterable

from ingestion import list_components
from reverse.models import PlanValidation, ReversePlan, RoutePlan


def validate_plan(plan: ReversePlan) -> PlanValidation:
    """Perform lightweight validation of inferred operations against the component registry."""
    existing_components = {component["component_name"] for component in list_components(plan.api_slug)}
    validation = PlanValidation()

    for route in plan.routes:
        if route.component and route.component not in existing_components:
            validation.errors.append(
                f"Route {route.method} {route.path} references unknown component '{route.component}'."
            )
        for warning in route.warnings:
            validation.warnings.append(f"{route.method} {route.path}: {warning}")

    plan.validation.errors.extend(validation.errors)
    plan.validation.warnings.extend(validation.warnings)
    return plan.validation


def has_blocking_errors(plan: ReversePlan) -> bool:
    return bool(plan.validation.errors)
