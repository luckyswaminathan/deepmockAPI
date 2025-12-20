"""Observation Encoder for RL state encoding."""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional, Set

from .goal_manager import GoalManager
from .models import State
from .state_manager import StateManager


class ObservationEncoder:
    """Encodes states into observations for RL policies."""
    
    def __init__(
        self,
        goal_manager: GoalManager,
        state_manager: StateManager,
        history_length: int = 5,
    ):
        self.goal_manager = goal_manager
        self.state_manager = state_manager
        self.history_length = history_length
    
    def encode_observation(
        self,
        goal_id: str,
        state_id: str,
        top_k_routes: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Encode a state into an observation for the policy.
        
        Args:
            goal_id: Goal ID
            state_id: Current state ID
            top_k_routes: Optional top-k routes from OpenAPI spec (for LLM policies)
        
        Returns:
            Observation dictionary with:
            - required: list of required component types
            - satisfied: list of satisfied component types
            - known_ids: dict mapping component type to list of IDs
            - last_k_components: last K modified components
            - last_action_id: last action ID
            - last_status: last response status
            - steps_remaining: estimated steps remaining (if available)
            - top_k_routes: top-k routes (if provided)
        """
        goal = self.goal_manager.get_goal(goal_id)
        state = self.state_manager.get_state(state_id, reconstruct_if_missing=True)
        
        # Extract required components from goal
        required_components = self._extract_required_components(goal.goal_state)
        
        # Determine which required components are satisfied
        satisfied_components = self._get_satisfied_components(
            required_components,
            state.modified_components,
        )
        
        # Extract known IDs by component type
        known_ids = self._extract_known_ids(state.modified_components)
        
        # Get recent history (last K components and actions)
        last_k_components, last_action_id, last_status = self._get_recent_history(
            state_id,
            state,
        )
        
        # Estimate steps remaining (simple heuristic: number of unsatisfied components)
        steps_remaining = len(required_components) - len(satisfied_components)
        
        observation = {
            "required": required_components,
            "satisfied": satisfied_components,
            "known_ids": known_ids,
            "last_k_components": last_k_components,
            "last_action_id": last_action_id,
            "last_status": last_status,
            "steps_remaining": steps_remaining,
        }
        
        # Add top-k routes if provided (for LLM policies)
        if top_k_routes is not None:
            observation["top_k_routes"] = top_k_routes
        
        return observation
    
    def _extract_required_components(self, goal_state: Dict[str, Any]) -> List[str]:
        """Extract list of required component types from goal state."""
        required = []
        
        if "target_components" in goal_state:
            required = list(goal_state["target_components"].keys())
        elif "target_conditions" in goal_state:
            # Extract unique component names from conditions
            conditions = goal_state["target_conditions"]
            required = list(set(c.get("component") for c in conditions if c.get("component")))
        else:
            # Treat goal_state as target_components
            required = list(goal_state.keys())
        
        return required
    
    def _get_satisfied_components(
        self,
        required_components: List[str],
        modified_components: Dict[str, List[Dict[str, Any]]],
    ) -> List[str]:
        """Determine which required components have been satisfied."""
        satisfied = []
        
        for component in required_components:
            if component in modified_components:
                records = modified_components[component]
                if records and len(records) > 0:
                    satisfied.append(component)
        
        return satisfied
    
    def _extract_known_ids(
        self,
        modified_components: Dict[str, List[Dict[str, Any]]],
    ) -> Dict[str, List[str]]:
        """Extract known entity IDs by component type."""
        known_ids = {}
        
        for component_name, records in modified_components.items():
            ids = []
            for record in records:
                # Try to extract ID from common fields
                record_id = (
                    record.get("id") or
                    record.get("record_key") or
                    record.get("_id") or
                    str(record.get("id", ""))
                )
                if record_id:
                    # Truncate long IDs for readability
                    id_str = str(record_id)
                    if len(id_str) > 8:
                        id_str = id_str[:8] + "..."
                    ids.append(id_str)
            
            if ids:
                known_ids[component_name] = ids
        
        return known_ids
    
    def _get_recent_history(
        self,
        state_id: str,
        state: State,
    ) -> tuple[List[str], Optional[str], Optional[int]]:
        """
        Get recent history: last K modified components, last action ID, last status.
        
        Returns:
            Tuple of (last_k_components, last_action_id, last_status)
        """
        # Get last K components from action path
        last_k_components = []
        last_action_id = None
        last_status = None
        
        if state.action_path:
            # Get last action ID
            last_action_id = state.action_path[-1]
            
            # Get last K actions and their components
            try:
                from .action_tracker import ActionTracker
                action_tracker = ActionTracker(self.state_manager)
                
                # Walk backwards through action path to get recent components
                recent_actions = state.action_path[-self.history_length:]
                components_seen = []
                
                for action_id in reversed(recent_actions):
                    try:
                        action = action_tracker.get_action(action_id)
                        if action.component_name:
                            components_seen.insert(0, action.component_name)
                        if last_status is None and action.response_status:
                            last_status = action.response_status
                    except (ValueError, ImportError):
                        # Action evicted or tracker unavailable, skip
                        continue
                
                last_k_components = components_seen[:self.history_length]
            except ImportError:
                # Action tracker not available, use component names from state
                last_k_components = []
        
        # If no action path, try to infer from current state's modified components
        if not last_k_components and state.modified_components:
            last_k_components = list(state.modified_components.keys())[-self.history_length:]
        
        return last_k_components, last_action_id, last_status

