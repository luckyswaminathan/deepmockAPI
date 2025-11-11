"""Pydantic models for RL entities."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class State(BaseModel):
    """Represents a state in the RL state space."""
    
    state_id: str = Field(default_factory=lambda: f"state_{uuid4().hex[:16]}")
    api_slug: str
    parent_state_id: Optional[str] = None
    action_path: List[str] = Field(default_factory=list)  # List of action_ids
    modified_components: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Action(BaseModel):
    """Represents an action (API call) that transitions between states."""
    
    action_id: str = Field(default_factory=lambda: f"action_{uuid4().hex[:16]}")
    state_id: str  # State before action
    next_state_id: str  # State after action
    method: str  # HTTP method (GET, POST, PUT, DELETE, PATCH)
    path: str  # API endpoint path
    params: Dict[str, Any] = Field(default_factory=dict)  # Path/query params
    request_body: Optional[Dict[str, Any]] = None
    response_status: int
    response_body: Optional[Dict[str, Any]] = None
    component_name: Optional[str] = None  # Component modified by this action
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Goal(BaseModel):
    """Represents a goal state for RL training."""
    
    goal_id: str = Field(default_factory=lambda: f"goal_{uuid4().hex[:16]}")
    api_slug: str
    description: Optional[str] = None
    start_state_id: str
    goal_state: Dict[str, Any]  # Target modified_components or conditions
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Episode(BaseModel):
    """Represents an RL episode (one attempt to reach a goal)."""
    
    episode_id: str = Field(default_factory=lambda: f"episode_{uuid4().hex[:16]}")
    goal_id: str
    current_state_id: str
    action_history: List[str] = Field(default_factory=list)  # List of action_ids
    reward: float = 0.0
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

