"""Pydantic models for reverse engineering workflows."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel
from reverse.models import RouteInventoryEntry


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
    use_graph: bool = False  # If True, generate data for ALL components using dependency graph
    seed_account_id: Optional[str] = None  # Optional account ID to associate data with
    # Note: OpenAI API key is read from OPENAI_API_KEY environment variable


class GenerateDataResponse(BaseModel):
    api_slug: str
    generated_at: datetime
    dataset: Dict[str, list[Dict[str, Any]]]
