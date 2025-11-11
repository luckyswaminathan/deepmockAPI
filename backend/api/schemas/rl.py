"""Pydantic models for RL API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# Goal Management
class CreateGoalRequest(BaseModel):
    api_slug: str
    goal_state: Dict[str, Any]  # target_components or target_conditions
    description: Optional[str] = None
    start_state_id: Optional[str] = None
    seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None


class GoalResponse(BaseModel):
    goal_id: str
    api_slug: str
    description: Optional[str]
    start_state_id: str
    goal_state: Dict[str, Any]
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


class ExecuteActionResponse(BaseModel):
    action_id: str
    next_state_id: str
    reward: float
    done: bool
    reason: str


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

