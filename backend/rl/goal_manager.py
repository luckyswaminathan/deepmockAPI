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
            # Support wildcard IDs (e.g., "cus_*" matches any customer ID)
            exact_matches = 0
            matched_current_record_ids = set()  # Track by record ID, not Python id()
            
            for target_record in target_records:
                target_id = str(target_record.get("id", target_record.get("record_key", "")))
                
                # Try to find matching current record
                for current_record in current_records:
                    # Get the record's actual ID (not Python's id())
                    current_record_id = str(current_record.get("id", current_record.get("record_key", "")))
                    
                    # Skip if already matched
                    if current_record_id in matched_current_record_ids:
                        continue
                    
                    # Check if records match (handles wildcards)
                    if self._records_match(current_record, target_record):
                        exact_matches += 1
                        matched_current_record_ids.add(current_record_id)
                        break  # One match per target record
            
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
        """
        Check if two records match (supports wildcards).
        
        Wildcards:
        - "*" matches anything (e.g., "cus_*" matches "cus_123", "cus_abc")
        - Field comparison: if target has a field, current must match (or be wildcard)
        """
        # Compare all fields in target record (record2 is the target/goal)
        for field, target_value in record2.items():
            current_value = record1.get(field)
            
            # If target is "*", it matches anything (including None)
            if str(target_value) == "*":
                continue
            
            # If target value is None, skip (optional field)
            if target_value is None:
                continue
            
            # If current value is None and target is not "*", no match
            if current_value is None:
                return False
            
            # Compare values (support wildcard matching)
            target_str = str(target_value)
            current_str = str(current_value)
            
            # If target ends with "*", check prefix match
            if target_str.endswith("*"):
                prefix = target_str[:-1]
                if not current_str.startswith(prefix):
                    return False
            # Otherwise, exact match
            elif current_str != target_str:
                return False
        
        return True
