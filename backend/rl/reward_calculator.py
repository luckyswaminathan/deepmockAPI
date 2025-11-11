"""Reward Calculator for RL reward computation."""

from __future__ import annotations

from typing import Optional

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
    ) -> tuple[float, bool, str]:
        """
        Compute reward for current state relative to goal.
        
        Args:
            goal_id: Goal ID
            current_state_id: Current state ID
            previous_state_id: Previous state ID (for progress-based rewards)
        
        Returns:
            Tuple of (reward, done, reason)
        """
        done, reward, reason = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        
        # Add progress-based reward if previous state provided
        if previous_state_id and not done:
            progress_reward = self._compute_progress_reward(
                goal_id, previous_state_id, current_state_id
            )
            # Combine goal reward with progress reward
            reward = 0.7 * reward + 0.3 * progress_reward
        
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

