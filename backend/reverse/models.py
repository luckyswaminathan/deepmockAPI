from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class RouteInventoryEntry(BaseModel):
    method: str
    path: str
    operation_id: Optional[str] = None
    summary: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    request_body_ref: Optional[str] = None
    response_body_ref: Optional[str] = None
    path_parameters: list[str] = Field(default_factory=list)
    query_parameters: list[str] = Field(default_factory=list)


class ReverseIngestionResult(BaseModel):
    api_slug: str
    api_name: str
    version: Optional[str]
    route_inventory: list[RouteInventoryEntry]


class OperationFilter(BaseModel):
    field: str
    operator: str = "eq"
    value_source: str


class OperationJoin(BaseModel):
    component: str
    on: str


class OperationPlan(BaseModel):
    type: str
    component: Optional[str]
    filters: list[OperationFilter] = Field(default_factory=list)
    joins: list[OperationJoin] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class RoutePlan(BaseModel):
    method: str
    path: str
    component: Optional[str]
    summary: Optional[str] = None
    operations: list[OperationPlan] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    status: str = "planned"


class PlanValidation(BaseModel):
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ReversePlan(BaseModel):
    api_slug: str
    generated_at: datetime
    routes: list[RoutePlan]
    validation: PlanValidation


class GenerationReport(BaseModel):
    api_slug: str
    output_dir: str
    files_written: list[str]


class PreviewEntry(BaseModel):
    path: str
    size_bytes: int
    updated_at: datetime


class PreviewResponse(BaseModel):
    api_slug: str
    files: list[PreviewEntry]
