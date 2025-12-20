"""Pydantic models for RL API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Goal Management
class RewardCondition(BaseModel):
    component: str
    field: str
    operator: str = "equals"
    value: Any
    reward: float = 0.1


class RewardConfig(BaseModel):
    invalid_status_penalty: float = -0.2
    success_bonus: float = 1.0
    progress_weight: float = 0.3
    custom_conditions: List[RewardCondition] = Field(default_factory=list)


class CreateGoalRequest(BaseModel):
    api_slug: str
    goal_state: Dict[str, Any]  # target_components or target_conditions
    description: Optional[str] = None
    start_state_id: Optional[str] = None
    seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None
    reward_config: Optional[RewardConfig] = None


class GoalResponse(BaseModel):
    goal_id: str
    api_slug: str
    description: Optional[str]
    start_state_id: str
    goal_state: Dict[str, Any]
    reward_config: Optional[RewardConfig]
    created_at: datetime


# Episode Management
class StartEpisodeRequest(BaseModel):
    goal_id: str


class EpisodeResponse(BaseModel):
    episode_id: str
    goal_id: str
    current_state_id: str
    action_history: List[str]
    reward: float
    done: bool
    created_at: datetime
    updated_at: datetime


class ExecuteActionRequest(BaseModel):
    method: str
    path: str
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None


class ExecuteActionResponse(BaseModel):
    action_id: str
    next_state_id: str
    reward: float
    done: bool
    reason: str
    response_status: int
    response_body: Optional[Any]


class ResetEpisodeRequest(BaseModel):
    state_id: Optional[str] = None  # If None, resets to start state


class ResetEpisodeResponse(BaseModel):
    episode_id: str
    current_state_id: str
    message: str


# State Management
class StateResponse(BaseModel):
    state_id: str
    api_slug: str
    parent_state_id: Optional[str]
    action_path: List[str]
    modified_components: Dict[str, List[Dict[str, Any]]]
    created_at: datetime


class StatePathResponse(BaseModel):
    state_id: str
    action_path: List[Dict[str, Any]]  # List of action objects


class StateChildrenResponse(BaseModel):
    state_id: str
    children: List[str]


class RestoreStateRequest(BaseModel):
    state_id: str
    initial_seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None


class RestoreStateResponse(BaseModel):
    state_id: str
    message: str


# Action Management
class ActionResponse(BaseModel):
    action_id: str
    state_id: str
    next_state_id: str
    method: str
    path: str
    params: Dict[str, Any]
    request_body: Optional[Dict[str, Any]]
    response_status: int
    response_body: Optional[Dict[str, Any]]
    component_name: Optional[str]
    timestamp: datetime


class ActionsListResponse(BaseModel):
    actions: List[ActionResponse]
    total: int


# Session Management (for tracking RL episodes)
class CreateSessionRequest(BaseModel):
    api_slug: str
    initial_state_id: Optional[str] = None
    seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None


class SessionResponse(BaseModel):
    session_id: str
    api_slug: str
    current_state_id: str
    start_state_id: str
    actions: List[str]
    created_at: datetime


# Observation and Action Masking
class ObservationResponse(BaseModel):
    """Observation for RL policy."""
    required: List[str]
    satisfied: List[str]
    known_ids: Dict[str, List[str]]
    last_k_components: List[str]
    last_action_id: Optional[str]
    last_status: Optional[int]
    steps_remaining: int
    top_k_routes: Optional[List[Dict[str, Any]]] = None


class ValidActionsResponse(BaseModel):
    """Valid actions at current state."""
    state_id: str
    valid_action_ids: List[str]
    total_actions: int


class TransitionInfo(BaseModel):
    """Info for a transition."""
    status: Optional[int] = None
    component_name: Optional[str] = None
    modified_components: Optional[Dict[str, List[Dict[str, Any]]]] = None


class TransitionResponse(BaseModel):
    """A single transition for PPO training."""
    state_id: str
    obs: Dict[str, Any]
    action_id: str
    reward: float
    done: bool
    next_state_id: str
    info: Dict[str, Any]
    timestamp: str


class EpisodeTransitionsResponse(BaseModel):
    """Transitions for an episode."""
    episode_id: str
    goal_id: str
    transitions: List[TransitionResponse]
    total_steps: int
    total_reward: float
    final_done: bool
