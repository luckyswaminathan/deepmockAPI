"""Pydantic models for RL entities."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class State(BaseModel):
    """Represents a state in the RL state space.
    
    Each state is a complete snapshot of the database at that point.
    States are created by copying the parent state's snapshot and applying new changes.
    """
    
    state_id: str = Field(default_factory=lambda: f"state_{uuid4().hex[:16]}")
    api_slug: str
    parent_state_id: Optional[str] = None
    action_path: List[str] = Field(default_factory=list)  # List of action_ids
    modified_components: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)  # Complete snapshot
    reward: Optional[float] = None  # Reward at this state (computed after action)
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


class RewardCondition(BaseModel):
    """Simple condition that awards additional reward when matched."""

    component: str
    field: str
    operator: str = "equals"  # equals, contains, gt, gte, lt, lte
    value: Any
    reward: float = 0.1


class RewardConfig(BaseModel):
    """Configuration for shaping rewards beyond basic goal completion."""

    invalid_status_penalty: float = -0.2
    success_bonus: float = 1.0
    progress_weight: float = 0.3
    custom_conditions: List[RewardCondition] = Field(default_factory=list)


class Goal(BaseModel):
    """Represents a goal state for RL training."""
    
    goal_id: str = Field(default_factory=lambda: f"goal_{uuid4().hex[:16]}")
    api_slug: str
    description: Optional[str] = None
    start_state_id: str
    goal_state: Dict[str, Any]  # Target modified_components or conditions
    reward_config: Optional[RewardConfig] = None
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
