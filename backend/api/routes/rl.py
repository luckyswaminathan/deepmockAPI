"""FastAPI router for RL state tracking endpoints."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

import httpx
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from ..schemas.rl import (
    CreateGoalRequest,
    CreateSessionRequest,
    EpisodeResponse,
    ExecuteActionRequest,
    ExecuteActionResponse,
    GoalResponse,
    ResetEpisodeRequest,
    ResetEpisodeResponse,
    RestoreStateRequest,
    RestoreStateResponse,
    SessionResponse,
    StartEpisodeRequest,
    StateChildrenResponse,
    StatePathResponse,
    StateResponse,
)
from rl.action_tracker import ActionTracker
from rl.goal_manager import GoalManager
from rl.models import Episode
from rl.redis_client import get_redis_client
from rl.reward_calculator import RewardCalculator
from rl.state_manager import StateManager
from rl.utils import json_to_model, model_to_json

router = APIRouter(prefix="/rl", tags=["rl"])

# Initialize managers
_state_manager = StateManager()
_action_tracker = ActionTracker(_state_manager)
_goal_manager = GoalManager(_state_manager)
_reward_calculator = RewardCalculator(_goal_manager, _state_manager)
_redis = get_redis_client()


# Goal Management
@router.post("/goals", response_model=GoalResponse)
def create_goal(payload: CreateGoalRequest) -> GoalResponse:
    """Create a new RL goal."""
    try:
        goal_id = _goal_manager.create_goal(
            api_slug=payload.api_slug,
            goal_state=payload.goal_state,
            description=payload.description,
            start_state_id=payload.start_state_id,
            seed_data=payload.seed_data,
            reward_config=payload.reward_config.dict() if payload.reward_config else None,
        )
        
        goal = _goal_manager.get_goal(goal_id)
        return GoalResponse(
            goal_id=goal.goal_id,
            api_slug=goal.api_slug,
            description=goal.description,
            start_state_id=goal.start_state_id,
            goal_state=goal.goal_state,
            reward_config=goal.reward_config,
            created_at=goal.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/goals/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: str) -> GoalResponse:
    """Get goal by ID."""
    try:
        goal = _goal_manager.get_goal(goal_id)
        return GoalResponse(
            goal_id=goal.goal_id,
            api_slug=goal.api_slug,
            description=goal.description,
            start_state_id=goal.start_state_id,
            goal_state=goal.goal_state,
            reward_config=goal.reward_config,
            created_at=goal.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Episode Management
@router.post("/goals/{goal_id}/episodes", response_model=EpisodeResponse)
def start_episode(goal_id: str, payload: StartEpisodeRequest) -> EpisodeResponse:
    """Start a new RL episode for a goal."""
    try:
        goal = _goal_manager.get_goal(goal_id)
        
        # Create episode
        episode_id = f"episode_{uuid4().hex[:16]}"
        episode = Episode(
            episode_id=episode_id,
            goal_id=goal_id,
            current_state_id=goal.start_state_id,
            action_history=[],
            reward=0.0,
            done=False,
        )
        
        # Store episode and seed session cache
        episode_json = model_to_json(episode)
        _redis.set(f"episode:{episode_id}", episode_json)
        _ensure_episode_session(episode, goal.api_slug)
        
        return EpisodeResponse(
            episode_id=episode.episode_id,
            goal_id=episode.goal_id,
            current_state_id=episode.current_state_id,
            action_history=episode.action_history,
            reward=episode.reward,
            done=episode.done,
            created_at=episode.created_at,
            updated_at=episode.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/episodes/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: str) -> EpisodeResponse:
    """Get episode by ID."""
    episode_json = _redis.get(f"episode:{episode_id}")
    if not episode_json:
        raise HTTPException(status_code=404, detail=f"Episode {episode_id} not found")
    
    episode = json_to_model(Episode, episode_json)
    return EpisodeResponse(
        episode_id=episode.episode_id,
        goal_id=episode.goal_id,
        current_state_id=episode.current_state_id,
        action_history=episode.action_history,
        reward=episode.reward,
        done=episode.done,
        created_at=episode.created_at,
        updated_at=episode.updated_at,
    )


@router.post("/episodes/{episode_id}/actions", response_model=ExecuteActionResponse)
async def execute_action(episode_id: str, payload: ExecuteActionRequest, request: Request) -> ExecuteActionResponse:
    """Execute an action by proxying to the generated API and tracking the result."""
    episode_json = _redis.get(f"episode:{episode_id}")
    if not episode_json:
        raise HTTPException(status_code=404, detail=f"Episode {episode_id} not found")
    episode = json_to_model(Episode, episode_json)
    if episode.done:
        raise HTTPException(status_code=400, detail="Episode is already done")
    goal = _goal_manager.get_goal(episode.goal_id)
    api_slug = goal.api_slug
    session_id = _ensure_episode_session(episode, api_slug)

    target_path = payload.path or "/"
    if not target_path.startswith("/"):
        target_path = f"/{target_path}"
    if not target_path.startswith("/generated/"):
        target_path = f"/generated/{api_slug}{target_path}"

    headers = dict(payload.headers or {})
    headers.setdefault("X-RL-Session-Id", session_id)
    headers.setdefault("X-RL-State-Id", episode.current_state_id)

    method = payload.method.upper()
    try:
        async with httpx.AsyncClient(app=request.app, base_url="http://rl-internal") as client:
            response = await client.request(
                method,
                target_path,
                params=payload.params or {},
                json=payload.body,
                headers=headers,
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to execute action: {exc}") from exc

    response_body: Any = None
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type.lower():
        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text
    else:
        response_body = response.text

    action_id = response.headers.get("X-RL-Action-Id")
    next_state_id = response.headers.get("X-RL-Next-State-Id") or episode.current_state_id
    if not action_id:
        action_id, next_state_id = _action_tracker.record_action(
            state_id=episode.current_state_id,
            method=method,
            path=target_path,
            params=payload.params or {},
            request_body=payload.body,
            response_status=response.status_code,
            response_body=response_body if isinstance(response_body, dict) else None,
        )

    previous_state_id = episode.current_state_id
    reward, done, reason = _reward_calculator.compute_reward(
        goal_id=episode.goal_id,
        current_state_id=next_state_id,
        previous_state_id=previous_state_id,
        response_status=response.status_code,
        response_body=response_body if isinstance(response_body, dict) else None,
    )

    episode.current_state_id = next_state_id
    episode.action_history.append(action_id)
    episode.reward = reward
    episode.done = done
    episode.updated_at = datetime.utcnow()
    episode_json = model_to_json(episode)
    _redis.set(f"episode:{episode_id}", episode_json)
    _update_episode_session(session_id, next_state_id, action_id)

    return ExecuteActionResponse(
        action_id=action_id,
        next_state_id=next_state_id,
        reward=reward,
        done=done,
        reason=reason,
        response_status=response.status_code,
        response_body=response_body,
    )


@router.post("/episodes/{episode_id}/reset", response_model=ResetEpisodeResponse)
def reset_episode(episode_id: str, payload: ResetEpisodeRequest) -> ResetEpisodeResponse:
    """Reset episode to start state or specified state."""
    episode_json = _redis.get(f"episode:{episode_id}")
    if not episode_json:
        raise HTTPException(status_code=404, detail=f"Episode {episode_id} not found")
    
    episode = json_to_model(Episode, episode_json)
    goal = _goal_manager.get_goal(episode.goal_id)
    
    # Determine target state
    target_state_id = payload.state_id or goal.start_state_id
    
    # Restore state
    _state_manager.restore_state(target_state_id)
    
    # Reset episode
    episode.current_state_id = target_state_id
    episode.action_history = []
    episode.reward = 0.0
    episode.done = False
    
    episode_json = model_to_json(episode)
    _redis.set(f"episode:{episode_id}", episode_json)
    
    return ResetEpisodeResponse(
        episode_id=episode_id,
        current_state_id=target_state_id,
        message=f"Episode reset to state {target_state_id}",
    )


# State Management
@router.get("/states/{state_id}", response_model=StateResponse)
def get_state(state_id: str) -> StateResponse:
    """Get state by ID."""
    try:
        state = _state_manager.get_state(state_id, reconstruct_if_missing=True)
        return StateResponse(
            state_id=state.state_id,
            api_slug=state.api_slug,
            parent_state_id=state.parent_state_id,
            action_path=state.action_path,
            modified_components=state.modified_components,
            created_at=state.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/states/{state_id}/path", response_model=StatePathResponse)
def get_state_path(state_id: str) -> StatePathResponse:
    """Get action path to reach a state."""
    try:
        state = _state_manager.get_state(state_id, reconstruct_if_missing=True)
        # Get action objects from action IDs
        actions = []
        for action_id in state.action_path:
            try:
                action = _action_tracker.get_action(action_id)
                actions.append({
                    "action_id": action.action_id,
                    "method": action.method,
                    "path": action.path,
                    "params": action.params,
                })
            except ValueError:
                # Action evicted, skip
                continue
        
        return StatePathResponse(
            state_id=state_id,
            action_path=actions,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/states/{state_id}/children", response_model=StateChildrenResponse)
def get_state_children(state_id: str) -> StateChildrenResponse:
    """Get child states of a state."""
    try:
        children = _state_manager.get_state_children(state_id)
        return StateChildrenResponse(
            state_id=state_id,
            children=children,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/states/{state_id}/restore", response_model=RestoreStateResponse)
def restore_state(state_id: str, payload: RestoreStateRequest) -> RestoreStateResponse:
    """Restore database to a specific state."""
    try:
        _state_manager.restore_state(
            state_id=payload.state_id,
            initial_seed_data=payload.initial_seed_data,
        )
        return RestoreStateResponse(
            state_id=payload.state_id,
            message=f"Database restored to state {payload.state_id}",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# Session Management (simpler interface for RL agents)
@router.post("/sessions", response_model=SessionResponse)
def create_session(payload: CreateSessionRequest) -> SessionResponse:
    """Create a new RL session."""
    session_id = f"session_{uuid4().hex[:16]}"
    
    # Get or create initial state
    if payload.initial_state_id:
        start_state_id = payload.initial_state_id
    else:
        start_state_id = _state_manager.get_initial_state(
            payload.api_slug, payload.seed_data
        )
    
    session_data = {
        "session_id": session_id,
        "api_slug": payload.api_slug,
        "current_state_id": start_state_id,
        "start_state_id": start_state_id,
        "actions": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    
    _redis.set(f"session:{session_id}", json.dumps(session_data))
    
    return SessionResponse(
        session_id=session_id,
        api_slug=payload.api_slug,
        current_state_id=start_state_id,
        start_state_id=start_state_id,
        actions=[],
        created_at=datetime.fromisoformat(session_data["created_at"]),
    )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str) -> SessionResponse:
    """Get session by ID."""
    session_json = _redis.get(f"session:{session_id}")
    if not session_json:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    session_data = json.loads(session_json)
    return SessionResponse(
        session_id=session_data["session_id"],
        api_slug=session_data["api_slug"],
        current_state_id=session_data["current_state_id"],
        start_state_id=session_data["start_state_id"],
        actions=session_data.get("actions", []),
        created_at=datetime.fromisoformat(session_data["created_at"]),
    )


def _ensure_episode_session(episode: Episode, api_slug: str) -> str:
    session_key = f"session:{episode.episode_id}"
    session_json = _redis.get(session_key)
    if session_json:
        data = json.loads(session_json)
        data["current_state_id"] = episode.current_state_id
        _redis.set(session_key, json.dumps(data))
        return data["session_id"]
    session_data = {
        "session_id": episode.episode_id,
        "api_slug": api_slug,
        "current_state_id": episode.current_state_id,
        "start_state_id": episode.current_state_id,
        "actions": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    _redis.set(session_key, json.dumps(session_data))
    return episode.episode_id


def _update_episode_session(session_id: str, state_id: str, action_id: str) -> None:
    session_key = f"session:{session_id}"
    session_json = _redis.get(session_key)
    if session_json:
        data = json.loads(session_json)
    else:
        data = {
            "session_id": session_id,
            "api_slug": "unknown",
            "current_state_id": state_id,
            "start_state_id": state_id,
            "actions": [],
            "created_at": datetime.utcnow().isoformat(),
        }
    data["current_state_id"] = state_id
    data.setdefault("actions", []).append(action_id)
    _redis.set(session_key, json.dumps(data))
