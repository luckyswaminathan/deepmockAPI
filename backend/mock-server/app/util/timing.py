from __future__ import annotations

import asyncio
from typing import Optional


async def apply_latency(latency_ms: Optional[int]) -> None:
    """Sleep for the requested latency (in milliseconds)."""
    if latency_ms is None:
        return
    if latency_ms < 0:
        latency_ms = 0
    await asyncio.sleep(latency_ms / 1000.0)
