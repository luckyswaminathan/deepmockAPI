from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RequestState:
    """Container for per-request parameters made available to factories."""

    path: Dict[str, Any] = field(default_factory=dict)
    query: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, Any] = field(default_factory=dict)
    body: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "query": self.query,
            "headers": self.headers,
            "body": self.body,
        }
