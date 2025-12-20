"""Action Tracker for recording API actions and state transitions."""

from __future__ import annotations

import sys
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4

from .models import Action
from .redis_client import get_redis_client
from .state_manager import StateManager
from .utils import model_to_json, json_to_model


class ActionTracker:
    """Tracks actions and manages state transitions."""
    
    def __init__(self, state_manager: Optional[StateManager] = None):
        self.redis = get_redis_client()
        self.state_manager = state_manager or StateManager()
    
    def _action_key(self, action_id: str) -> str:
        """Get Redis key for an action."""
        return f"action:{action_id}"
    
    def _state_actions_key(self, state_id: str) -> str:
        """Get Redis key for state actions set."""
        return f"state:{state_id}:actions"
    
    def record_action(
        self,
        state_id: str,
        method: str,
        path: str,
        params: Dict[str, Any],
        request_body: Optional[Dict[str, Any]],
        response_status: int,
        response_body: Optional[Dict[str, Any]],
        component_name: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Record an action and create the next state.
        
        Args:
            state_id: Current state ID (before action)
            method: HTTP method
            path: API endpoint path
            params: Path/query parameters
            request_body: Request body (if any)
            response_status: HTTP response status code
            response_body: Response body (if any)
            component_name: Component modified by this action (if known)
        
        Returns:
            Tuple of (action_id, next_state_id)
        """
        # Detect which component was modified
        # If component_name not provided, try to infer from path or response
        if component_name is None:
            component_name = self._infer_component_name(path, method, response_body)
        
        # Create action record
        action_id = f"action_{uuid4().hex[:16]}"
        action = Action(
            action_id=action_id,
            state_id=state_id,
            next_state_id="",  # Will be set after creating next state
            method=method,
            path=path,
            params=params,
            request_body=request_body,
            response_status=response_status,
            response_body=response_body,
            component_name=component_name,
        )
        
        # Detect modified components from database changes
        # Get current state to know what API we're working with
        current_state = self.state_manager.get_state(state_id, reconstruct_if_missing=True)
        api_slug = current_state.api_slug
        
        # IMPORTANT: To ensure states are independent snapshots, we need to:
        # 1. Restore parent state to database (if parent exists)
        # 2. Then detect what changed from THIS action only
        # However, restoring state before every action would be expensive.
        # Instead, we compare current DB to parent state snapshot, which should work
        # as long as the parent state snapshot is complete.
        
        # Detect what changed (compare current DB state with parent state snapshot)
        modified_components = self.state_manager.detect_modified_components(
            api_slug, parent_state_id=state_id
        )
        
        # If we know the component name but it's not in modified_components,
        # add it with the response data
        if component_name and component_name not in modified_components:
            if response_body and isinstance(response_body, dict):
                # Use response body as the record
                modified_components[component_name] = [response_body]
            elif response_status == 200 and method in ("POST", "PUT", "PATCH"):
                # For successful mutations, response usually contains the created/updated object
                if response_body:
                    modified_components[component_name] = [response_body]
        
        # Create next state
        next_state_id = self.state_manager.create_state(
            api_slug=api_slug,
            parent_state_id=state_id,
            action_id=action_id,
            modified_components=modified_components,
        )
        
        # Update action with next_state_id
        action.next_state_id = next_state_id
        
        # Store action in Redis
        action_json = model_to_json(action)
        self.redis.set(self._action_key(action_id), action_json)
        
        # Link action to state
        self.redis.sadd(self._state_actions_key(state_id), action_id)
        
        print(
            f"[ActionTracker] Recorded action {action_id}: {method} {path} "
            f"({state_id} -> {next_state_id})",
            file=sys.stderr
        )
        
        return action_id, next_state_id
    
    def _infer_component_name(
        self, path: str, method: str, response_body: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Infer component name from path or response.
        
        Examples:
            /v1/accounts -> "account"
            /v1/customers/{id} -> "customer"
            /v1/accounts/{account}/bank_accounts -> "external_account"
        """
        # Simple heuristic: take the last resource name from path
        # Remove leading/trailing slashes and split
        parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
        
        if not parts:
            return None
        
        # Get the last part (resource name)
        resource = parts[-1]
        
        # Convert plural to singular (simple heuristic)
        if resource.endswith("ies"):
            component = resource[:-3] + "y"
        elif resource.endswith("s") and len(resource) > 1:
            component = resource[:-1]
        else:
            component = resource
        
        # Convert to snake_case if needed
        component = component.replace("-", "_").replace("_", "").lower()
        
        return component
    
    def get_action(self, action_id: str) -> Action:
        """Get action by ID."""
        action_json = self.redis.get(self._action_key(action_id))
        if not action_json:
            raise ValueError(f"Action {action_id} not found")
        return json_to_model(Action, action_json)
    
    def get_state_actions(self, state_id: str) -> list[Action]:
        """Get all actions from a state."""
        action_ids = self.redis.smembers(self._state_actions_key(state_id))
        actions = []
        for action_id in action_ids:
            try:
                actions.append(self.get_action(action_id))
            except ValueError:
                # Action might have been evicted, skip
                continue
        return actions
    
    def list_all_actions(self, limit: Optional[int] = None) -> list[Action]:
        """List all actions by scanning Redis keys."""
        actions = []
        cursor = 0
        pattern = "action:*"
        
        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
            for key in keys:
                try:
                    # Extract action_id from key (remove "action:" prefix)
                    action_id = key.replace("action:", "", 1)
                    action = self.get_action(action_id)
                    actions.append(action)
                    if limit and len(actions) >= limit:
                        return actions
                except ValueError:
                    # Action might have been evicted, skip
                    continue
            
            if cursor == 0:
                break
        
        return actions

