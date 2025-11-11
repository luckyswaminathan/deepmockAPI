"""Reward Calculator for RL reward computation."""

from __future__ import annotations

from typing import Any, Optional

from .goal_manager import GoalManager
from .state_manager import StateManager


class RewardCalculator:
    """Calculates rewards for RL agents based on goal progress."""
    
    def __init__(self, goal_manager: GoalManager, state_manager: StateManager):
        self.goal_manager = goal_manager
        self.state_manager = state_manager
    
    def compute_reward(
        self,
        goal_id: str,
        current_state_id: str,
        previous_state_id: Optional[str] = None,
        response_status: Optional[int] = None,
        response_body: Optional[Any] = None,
    ) -> tuple[float, bool, str]:
        """Compute shaped reward for the given goal/state."""
        goal = self.goal_manager.get_goal(goal_id)
        done, reward, reason = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        config = goal.reward_config
        
        # Customize success reward if provided
        if done and config and config.success_bonus is not None:
            reward = config.success_bonus
        
        # Add progress-based reward if previous state provided
        if previous_state_id and not done:
            progress_reward = self._compute_progress_reward(
                goal_id, previous_state_id, current_state_id
            )
            weight = config.progress_weight if config else 0.3
            reward = (1 - weight) * reward + weight * progress_reward
        
        # Response-based penalties/bonuses
        if config:
            reward += self._apply_response_penalties(config, response_status)
            reward += self._apply_custom_conditions(config, current_state_id)
        
        # Clamp reward to sensible range
        reward = max(-1.0, min(1.5, reward))
        return reward, done, reason
    
    def _compute_progress_reward(
        self,
        goal_id: str,
        previous_state_id: str,
        current_state_id: str,
    ) -> float:
        """
        Compute reward based on progress towards goal.
        
        Returns reward between 0.0 and 1.0 based on how much closer
        we are to the goal compared to previous state.
        """
        goal = self.goal_manager.get_goal(goal_id)
        previous_state = self.state_manager.get_state(previous_state_id, reconstruct_if_missing=True)
        current_state = self.state_manager.get_state(current_state_id, reconstruct_if_missing=True)
        
        # Compare how close previous and current states are to goal
        _, prev_reward, _ = self.goal_manager.check_goal_reached(goal_id, previous_state_id)
        _, curr_reward, _ = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        
        # Progress reward: positive if we got closer, negative if we got further
        progress = curr_reward - prev_reward
        
        # Normalize to 0-1 range (progress can be negative)
        # If progress is positive, reward it; if negative, penalize it
        if progress > 0:
            return min(1.0, progress * 2)  # Scale up positive progress
        else:
            return max(0.0, 1.0 + progress)  # Scale down negative progress
    
    def _apply_response_penalties(
        self,
        config,
        response_status: Optional[int],
    ) -> float:
        if response_status is None:
            return 0.0
        if response_status >= 400:
            return config.invalid_status_penalty
        return 0.0

    def _apply_custom_conditions(
        self,
        config,
        current_state_id: str,
    ) -> float:
        if not config.custom_conditions:
            return 0.0
        state = self.state_manager.get_state(current_state_id, reconstruct_if_missing=True)
        bonus = 0.0
        for condition in config.custom_conditions:
            records = state.modified_components.get(condition.component, [])
            if any(self._record_matches_condition(record, condition) for record in records):
                bonus += condition.reward
        return bonus

    def _record_matches_condition(self, record: dict[str, Any], condition) -> bool:
        value = record.get(condition.field)
        target = condition.value
        op = (condition.operator or "equals").lower()
        if op == "equals":
            return str(value) == str(target)
        if op == "contains":
            return target in value if isinstance(value, (list, str)) else False
        if op == "gt":
            return value is not None and target is not None and value > target
        if op == "gte":
            return value is not None and target is not None and value >= target
        if op == "lt":
            return value is not None and target is not None and value < target
        if op == "lte":
            return value is not None and target is not None and value <= target
        return False

    def compute_sparse_reward(
        self,
        goal_id: str,
        current_state_id: str,
    ) -> tuple[float, bool]:
        """
        Compute sparse reward (only reward when goal reached).
        
        Returns:
            Tuple of (reward, done)
        """
        done, _, _ = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        reward = 1.0 if done else 0.0
        return reward, done
    
    def compute_dense_reward(
        self,
        goal_id: str,
        current_state_id: str,
        previous_state_id: Optional[str] = None,
    ) -> tuple[float, bool]:
        """
        Compute dense reward (reward progress towards goal).
        
        Returns:
            Tuple of (reward, done)
        """
        return self.compute_reward(goal_id, current_state_id, previous_state_id)[:2]
