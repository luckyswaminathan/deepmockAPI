"""Pydantic models for primary ingestion and component APIs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ComponentResponse(BaseModel):
    component_name: str
    storage_key: str
    property_count: int


class IngestionResponse(BaseModel):
    api_slug: str
    api_name: str
    version: Optional[str]
    components: list[ComponentResponse]


class ApiSummary(BaseModel):
    api_slug: str
    api_name: str
    title: str
    version: Optional[str] = None
    created_at: datetime


class ComponentMeta(BaseModel):
    component_name: str
    storage_key: str
    property_count: int
    created_at: datetime


class PropertyRow(BaseModel):
    position: Optional[int] = None
    property_name: str
    property_type: Optional[str] = None
    property_format: Optional[str] = None
    is_required: bool
    description: Optional[str] = None
    example: Optional[Any] = None
    reference: Optional[str] = None


class ComponentDetail(BaseModel):
    component_name: str
    storage_key: Optional[str] = None
    component_schema: Dict[str, Any]
    properties: list[PropertyRow]


class ComponentGraphNode(BaseModel):
    component_name: str
    storage_key: str
    created_at: datetime
    property_count: int
    references: list[str]
    dependent_count: int


class ComponentGraphEdge(BaseModel):
    source: str
    target: str


class ComponentGraph(BaseModel):
    nodes: list[ComponentGraphNode]
    edges: list[ComponentGraphEdge]
