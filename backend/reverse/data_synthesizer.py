from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional
import os

from ingestion import get_component_entry, get_component_properties
from reverse.models import ReversePlan, RoutePlan
from reverse.planner import build_plan, load_route_inventory


def ensure_plan(api_slug: str, plan: Optional[ReversePlan] = None) -> ReversePlan:
    return plan or build_plan(api_slug, route_inventory=load_route_inventory(api_slug))


def synthesize(
    plan: ReversePlan,
    count_by_component: Optional[Dict[str, int]] = None,
    seed: int = 1337,
    use_graph: bool = False,
    openai_api_key: Optional[str] = None,
) -> Dict[str, list[dict]]:
    """
    Synthesize sample data for components.
    
    If use_graph=True, uses graph-based generation (all components, topological order).
    Otherwise, uses route-based generation (only components referenced in routes).
    
    Note: OpenAI API key is read from OPENAI_API_KEY env var if use_graph=True.
    """
    if use_graph:
        # Use graph-based generator for all components
        # OpenAI API key is read from OPENAI_API_KEY environment variable
        try:
            from reverse.graph_based_generator import GraphDataGenerator
            generator = GraphDataGenerator(plan.api_slug, openai_api_key)
            return generator.generate_all(count_by_component)
        except ImportError:
            # Fall back to route-based if graph generator unavailable
            pass
    
    # Original route-based synthesis
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


def synthesize_all_components(
    api_slug: str,
    count_per_component: Optional[Dict[str, int]] = None,
    openai_api_key: Optional[str] = None,
    seed_account_id: Optional[str] = None,
    store_in_db: bool = True,
) -> Dict[str, list[dict]]:
    """
    Generate sample data for ALL components in the API using dependency graph.
    
    This generates data for every component in the component registry, not just
    those referenced in routes. It follows dependency order (leaves first).
    
    Args:
        api_slug: API identifier
        count_per_component: Number of records per component (default: 3)
        openai_api_key: Optional OpenAI API key (overrides OPENAI_API_KEY env var)
        seed_account_id: Optional account ID to associate generated data with
        store_in_db: If True, store records in GeneratedRecord table (default: True)
    
    Returns:
        Dict mapping component_name -> list of records
    
    Note: OpenAI API key is read from OPENAI_API_KEY env var if not provided.
    
    Raises:
        ValueError: If API not found or has no components in the database.
    """
    from reverse.graph_based_generator import GraphDataGenerator
    from ingestion import list_components
    import sys
    import os
    
    # Debug: Print database connection being used
    db_url = os.getenv("_DATABASE_URL", os.getenv("DATABASE_URL", "NOT SET"))
    db_info = db_url.split('@')[-1] if '@' in db_url else db_url
    print(f"[synthesize_all_components] Checking components for '{api_slug}' using database: {db_info}", file=sys.stderr)
    
    # Check if API has components first
    components = list_components(api_slug)
    print(f"[synthesize_all_components] Found {len(components)} components for '{api_slug}'", file=sys.stderr)
    
    if not components:
        raise ValueError(
            f"API '{api_slug}' not found or has no components. "
            "Make sure to upload the OpenAPI spec via /apis/upload first."
        )
    
    generator = GraphDataGenerator(api_slug, openai_api_key)
    
    return generator.generate_all(count_per_component, seed_account_id, store_in_db=store_in_db)


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
