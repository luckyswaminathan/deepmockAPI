"""Goal Manager for RL goal definition and matching."""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .models import Goal, RewardConfig
from .redis_client import get_redis_client
from .state_manager import StateManager
from .utils import model_to_json, json_to_model


class GoalManager:
    """Manages RL goals: creation, storage, and goal state matching."""
    
    def __init__(self, state_manager: Optional[StateManager] = None):
        self.redis = get_redis_client()
        self.state_manager = state_manager or StateManager()
    
    def _goal_key(self, goal_id: str) -> str:
        """Get Redis key for a goal."""
        return f"goal:{goal_id}"
    
    def _api_goals_key(self, api_slug: str) -> str:
        """Get Redis key for API goals index."""
        return f"api:{api_slug}:goals"
    
    def create_goal(
        self,
        api_slug: str,
        goal_state: Dict[str, Any],
        description: Optional[str] = None,
        start_state_id: Optional[str] = None,
        seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        reward_config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a new goal.
        
        Args:
            api_slug: API identifier
            goal_state: Target state specification
                - Can be {"target_components": {...}} for exact match
                - Or {"target_conditions": [...]} for condition-based match
            description: Human-readable description
            start_state_id: Starting state ID (if None, creates initial state)
            seed_data: Seed data for initial state (if start_state_id not provided)
        
        Returns:
            goal_id
        """
        # Create or get start state
        if start_state_id is None:
            start_state_id = self.state_manager.get_initial_state(api_slug, seed_data)
        
        # Create goal
        goal_id = f"goal_{uuid4().hex[:16]}"
        config_obj = None
        if reward_config:
            config_obj = reward_config if isinstance(reward_config, RewardConfig) else RewardConfig(**reward_config)

        goal = Goal(
            goal_id=goal_id,
            api_slug=api_slug,
            description=description,
            start_state_id=start_state_id,
            goal_state=goal_state,
            reward_config=config_obj,
        )
        
        # Store in Redis
        goal_json = model_to_json(goal)
        self.redis.set(self._goal_key(goal_id), goal_json)
        
        # Update API goals index
        self.redis.sadd(self._api_goals_key(api_slug), goal_id)
        
        print(f"[GoalManager] Created goal {goal_id} for {api_slug}", file=sys.stderr)
        return goal_id
    
    def get_goal(self, goal_id: str) -> Goal:
        """Get goal by ID."""
        goal_json = self.redis.get(self._goal_key(goal_id))
        if not goal_json:
            raise ValueError(f"Goal {goal_id} not found")
        return json_to_model(Goal, goal_json)
    
    def check_goal_reached(self, goal_id: str, current_state_id: str) -> tuple[bool, float, str]:
        """
        Check if goal is reached and compute reward.
        
        Args:
            goal_id: Goal ID
            current_state_id: Current state ID
        
        Returns:
            Tuple of (done, reward, reason)
        """
        goal = self.get_goal(goal_id)
        current_state = self.state_manager.get_state(current_state_id, reconstruct_if_missing=True)
        
        goal_state = goal.goal_state
        
        # Check if goal uses target_components (exact match) or target_conditions
        if "target_components" in goal_state:
            return self._check_component_match(
                current_state.modified_components,
                goal_state["target_components"],
            )
        elif "target_conditions" in goal_state:
            return self._check_condition_match(
                current_state.modified_components,
                goal_state["target_conditions"],
            )
        else:
            # Default: treat goal_state as target_components
            return self._check_component_match(
                current_state.modified_components,
                goal_state,
            )
    
    def _check_component_match(
        self,
        current_components: Dict[str, List[Dict[str, Any]]],
        target_components: Dict[str, List[Dict[str, Any]]],
    ) -> tuple[bool, float, str]:
        """
        Check if current components match target components.
        
        Returns:
            (done, reward, reason)
        """
        if not target_components:
            return True, 1.0, "Goal has no target components (empty goal)"
        
        total_components = len(target_components)
        matched_components = 0
        partial_matches = 0
        
        for component_name, target_records in target_components.items():
            current_records = current_components.get(component_name, [])
            
            if not target_records:
                # Empty target means component should not exist or be empty
                if not current_records:
                    matched_components += 1
                continue
            
            if not current_records:
                # Component doesn't exist in current state
                continue
            
            # Check if any current record matches any target record
            # For now, simple matching: check if records with same IDs match
            target_map = {
                str(r.get("id", r.get("record_key", ""))): r
                for r in target_records
            }
            current_map = {
                str(r.get("id", r.get("record_key", ""))): r
                for r in current_records
            }
            
            # Check for exact matches
            exact_matches = 0
            for record_id, target_record in target_map.items():
                if record_id in current_map:
                    current_record = current_map[record_id]
                    # Check if records match (simplified: check key fields)
                    if self._records_match(current_record, target_record):
                        exact_matches += 1
            
            if exact_matches == len(target_records):
                matched_components += 1
            elif exact_matches > 0:
                partial_matches += 1
        
        # Compute reward
        if matched_components == total_components:
            return True, 1.0, f"All {total_components} components match"
        elif matched_components > 0 or partial_matches > 0:
            reward = (matched_components + partial_matches * 0.5) / total_components
            return False, reward, f"{matched_components}/{total_components} components match, {partial_matches} partial"
        else:
            return False, 0.0, "No components match"
    
    def _check_condition_match(
        self,
        current_components: Dict[str, List[Dict[str, Any]]],
        target_conditions: list[Dict[str, Any]],
    ) -> tuple[bool, float, str]:
        """
        Check if current state matches target conditions.
        
        Conditions format: [{"component": "account", "field": "name", "value": "Acme Inc"}]
        
        Returns:
            (done, reward, reason)
        """
        if not target_conditions:
            return True, 1.0, "No target conditions (empty goal)"
        
        total_conditions = len(target_conditions)
        matched_conditions = 0
        
        for condition in target_conditions:
            component_name = condition.get("component")
            field = condition.get("field")
            target_value = condition.get("value")
            
            if not component_name or not field:
                continue
            
            # Find matching record in current components
            records = current_components.get(component_name, [])
            for record in records:
                if str(record.get(field)) == str(target_value):
                    matched_conditions += 1
                    break
        
        # Compute reward
        if matched_conditions == total_conditions:
            return True, 1.0, f"All {total_conditions} conditions match"
        elif matched_conditions > 0:
            reward = matched_conditions / total_conditions
            return False, reward, f"{matched_conditions}/{total_conditions} conditions match"
        else:
            return False, 0.0, "No conditions match"
    
    def _records_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Check if two records match (simplified comparison)."""
        # For now, compare key fields
        # Could be enhanced to do deep comparison or field-specific matching
        key_fields = ["id", "name", "status", "type"]
        
        for field in key_fields:
            val1 = record1.get(field)
            val2 = record2.get(field)
            if val1 is not None and val2 is not None:
                if str(val1) != str(val2):
                    return False
        
        return True
