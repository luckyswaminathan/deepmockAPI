from __future__ import annotations

from typing import Any, Dict

def generate_components(count_by_component: Dict[str, int], seed: int = 1337) -> Dict[str, list[dict[str, Any]]]:
    """Deterministic sample data generator stub."""
    return {name: [{} for _ in range(count)] for name, count in count_by_component.items()}
