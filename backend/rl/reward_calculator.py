"""Reward Calculator for RL reward computation."""

from __future__ import annotations

from typing import Any, Dict, Optional, Set

from .goal_manager import GoalManager
from .state_manager import StateManager


class RewardCalculator:
    """Calculates rewards for RL agents based on goal progress."""
    
    def __init__(self, goal_manager: GoalManager, state_manager: StateManager):
        self.goal_manager = goal_manager
        self.state_manager = state_manager
        # Track satisfied components per episode to prevent farming
        self._episode_satisfied_components: Dict[str, Set[str]] = {}
        # Track step counts per episode for step penalty
        self._episode_step_counts: Dict[str, int] = {}
    
    def compute_reward(
        self,
        goal_id: str,
        current_state_id: str,
        previous_state_id: Optional[str] = None,
        response_status: Optional[int] = None,
        response_body: Optional[Any] = None,
        episode_id: Optional[str] = None,
    ) -> tuple[float, bool, str]:
        """
        Compute reward with proper shaping:
        - Prevents component farming (only reward first-time satisfaction)
        - Penalizes useless steps
        - Penalizes failures
        
        Args:
            goal_id: Goal ID
            current_state_id: Current state ID
            previous_state_id: Previous state ID (optional)
            response_status: HTTP response status code
            response_body: Response body (optional)
            episode_id: Episode ID for tracking satisfied components
        
        Returns:
            Tuple of (reward, done, reason)
        """
        goal = self.goal_manager.get_goal(goal_id)
        start_state_id = goal.start_state_id
        
        # Initialize episode tracking (if episode_id provided)
        already_satisfied = set()
        if episode_id:
            if episode_id not in self._episode_satisfied_components:
                self._episode_satisfied_components[episode_id] = set()
            if episode_id not in self._episode_step_counts:
                self._episode_step_counts[episode_id] = 0
            self._episode_step_counts[episode_id] += 1
            already_satisfied = self._episode_satisfied_components[episode_id]
        
        # Check if goal is reached
        done, current_reward, reason = self.goal_manager.check_goal_reached(goal_id, current_state_id)
        
        # If goal reached, give success reward
        if done:
            config = goal.reward_config
            success_reward = config.success_bonus if (config and config.success_bonus is not None) else 1.0
            # Clear episode tracking
            if episode_id:
                self._episode_satisfied_components.pop(episode_id, None)
                self._episode_step_counts.pop(episode_id, None)
            return success_reward, True, reason
        
        # Extract required components from goal
        required_components = self._extract_required_components(goal.goal_state)
        
        # Get current state to check which components are satisfied
        current_state = self.state_manager.get_state(current_state_id, reconstruct_if_missing=True)
        
        # Compute component completion reward (prevent farming)
        component_reward = 0.0
        newly_satisfied = []
        
        for component in required_components:
            if component in current_state.modified_components:
                records = current_state.modified_components[component]
                if records and len(records) > 0:
                    # Component is satisfied
                    if component not in already_satisfied:
                        # First time satisfying this component - give reward
                        component_reward += 1.0 / len(required_components)
                        newly_satisfied.append(component)
                        if episode_id:
                            already_satisfied.add(component)
        
        # Step penalty: small cost per step to encourage shortest solutions
        step_penalty = -0.01
        
        # Failure penalty: penalize errors more strongly
        failure_penalty = 0.0
        if response_status and response_status >= 400:
            # Stronger penalty for failures
            if response_status >= 500:
                failure_penalty = -0.3  # Server errors are worse
            else:
                failure_penalty = -0.2  # Client errors
        
        # Total reward
        reward = component_reward + step_penalty + failure_penalty
        
        # Build reason string
        reason_parts = []
        if newly_satisfied:
            reason_parts.append(f"satisfied: {', '.join(newly_satisfied)}")
        if failure_penalty < 0:
            reason_parts.append(f"error: {response_status}")
        reason = "; ".join(reason_parts) if reason_parts else "no progress"
        
        # Clamp to reasonable range
        reward = max(-1.0, min(1.0, reward))
        
        return reward, False, reason
    
    def _extract_required_components(self, goal_state: Dict[str, Any]) -> list[str]:
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
    
    def reset_episode_tracking(self, episode_id: str) -> None:
        """Reset tracking for an episode (call when episode starts/resets)."""
        self._episode_satisfied_components.pop(episode_id, None)
        self._episode_step_counts.pop(episode_id, None)
    
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
