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
        """
        Compute simple reward: progress from start state toward goal.
        
        Reward is positive if closer to goal than start state, negative if further.
        One episode = one attempt from start state to goal.
        """
        goal = self.goal_manager.get_goal(goal_id)
        start_state_id = goal.start_state_id
        
        # Check if goal is reached
        done, current_reward, reason = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        
        # If goal reached, give success reward
        if done:
            config = goal.reward_config
            success_reward = config.success_bonus if (config and config.success_bonus is not None) else 1.0
            return success_reward, True, reason
        
        # Compare current state to START state (not previous state)
        # This gives reward based on progress from beginning of episode
        _, start_reward, _ = self.goal_manager.check_goal_reached(goal_id, start_state_id)
        
        # Simple reward: how much closer are we to goal compared to start?
        progress = current_reward - start_reward
        
        # Reward is the progress (can be negative if we got further)
        reward = progress
        
        # Small penalty for errors (but don't override progress)
        if response_status and response_status >= 400:
            error_penalty = -0.1  # Small penalty, don't overwhelm progress signal
            reward += error_penalty
        
        # Clamp to reasonable range
        reward = max(-1.0, min(1.0, reward))
        
        return reward, False, reason
    
    def _compute_progress_reward(
        self,
        goal_id: str,
        previous_state_id: str,
        current_state_id: str,
    ) -> float:
        """
        Compute reward based on progress towards goal.
        
        Returns reward between -1.0 and 1.0 based on how much closer
        we are to the goal compared to previous state.
        """
        goal = self.goal_manager.get_goal(goal_id)
        previous_state = self.state_manager.get_state(previous_state_id, reconstruct_if_missing=True)
        current_state = self.state_manager.get_state(current_state_id, reconstruct_if_missing=True)
        
        # Compare how close previous and current states are to goal
        _, prev_reward, _ = self.goal_manager.check_goal_reached(goal_id, previous_state_id)
        _, curr_reward, _ = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        
        # Progress reward: positive if we got closer, negative if we got further, 0 if no change
        progress = curr_reward - prev_reward
        
        # Return progress directly (can be negative, zero, or positive)
        # Scale positive progress up, keep negative progress as penalty
        if progress > 0:
            return min(1.0, progress * 2)  # Scale up positive progress
        elif progress < 0:
            return max(-1.0, progress * 2)  # Scale down negative progress (penalty)
        else:
            return 0.0  # No progress = no reward (was incorrectly returning 1.0)
    
    def _apply_response_penalties(
        self,
        config,
        response_status: Optional[int],
    ) -> float:
        if response_status is None:
            return 0.0
        if response_status >= 400:
            # Apply penalty even if config is None (use default)
            penalty = config.invalid_status_penalty if config else -0.2
            # Scale penalty by error severity
            if response_status >= 500:
                return penalty * 1.5  # Server errors are worse
            elif response_status >= 400:
                return penalty  # Client errors
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
