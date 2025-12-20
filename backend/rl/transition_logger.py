"""Transition Logger for recording PPO rollout data."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .observation_encoder import ObservationEncoder
from .redis_client import get_redis_client


class TransitionLogger:
    """Logs transitions for PPO training data."""
    
    def __init__(
        self,
        observation_encoder: ObservationEncoder,
        log_dir: Optional[Path] = None,
    ):
        self.observation_encoder = observation_encoder
        self.redis = get_redis_client()
        self.log_dir = log_dir or Path("/tmp/rl_rollouts")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory buffer for current episode
        self.current_episode_transitions: List[Dict[str, Any]] = []
    
    def log_transition(
        self,
        goal_id: str,
        state_id: str,
        action_id: str,
        reward: float,
        done: bool,
        next_state_id: str,
        info: Optional[Dict[str, Any]] = None,
        top_k_routes: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Log a single transition for PPO training.
        
        Args:
            goal_id: Goal ID
            state_id: State before action
            action_id: Action taken
            reward: Reward received
            done: Whether episode is done
            next_state_id: State after action
            info: Additional info (status, component_name, modified_components, etc.)
            top_k_routes: Optional top-k routes for LLM policies
        """
        # Encode observation for this state
        obs = self.observation_encoder.encode_observation(
            goal_id=goal_id,
            state_id=state_id,
            top_k_routes=top_k_routes,
        )
        
        transition = {
            "state_id": state_id,
            "obs": obs,
            "action_id": action_id,
            "reward": reward,
            "done": done,
            "next_state_id": next_state_id,
            "info": info or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Add to current episode buffer
        self.current_episode_transitions.append(transition)
        
        # Also store in Redis for quick access
        episode_key = f"rollout:{goal_id}:transitions"
        transition_json = json.dumps(transition)
        self.redis.lpush(episode_key, transition_json)
        
        # Keep only last 1000 transitions in Redis (to avoid memory issues)
        self.redis.ltrim(episode_key, 0, 999)
    
    def finalize_episode(
        self,
        goal_id: str,
        episode_id: str,
        save_to_file: bool = True,
    ) -> Optional[Path]:
        """
        Finalize episode and save transitions to file.
        
        Args:
            goal_id: Goal ID
            episode_id: Episode ID
            save_to_file: Whether to save to file
        
        Returns:
            Path to saved file (if saved)
        """
        if not self.current_episode_transitions:
            return None
        
        # Get all transitions from Redis
        episode_key = f"rollout:{goal_id}:transitions"
        transition_jsons = self.redis.lrange(episode_key, 0, -1)
        
        # Parse transitions
        transitions = [json.loads(tj) for tj in transition_jsons]
        
        # Sort by timestamp
        transitions.sort(key=lambda t: t.get("timestamp", ""))
        
        # Create episode data
        episode_data = {
            "episode_id": episode_id,
            "goal_id": goal_id,
            "transitions": transitions,
            "total_steps": len(transitions),
            "total_reward": sum(t["reward"] for t in transitions),
            "final_done": transitions[-1]["done"] if transitions else False,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        if save_to_file:
            # Save to file
            filename = f"episode_{episode_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.log_dir / filename
            
            with filepath.open("w", encoding="utf-8") as f:
                json.dump(episode_data, f, indent=2, default=str)
            
            print(
                f"[TransitionLogger] Saved {len(transitions)} transitions to {filepath}",
                file=sys.stderr
            )
            
            # Clear Redis buffer
            self.redis.delete(episode_key)
            
            # Clear in-memory buffer
            self.current_episode_transitions = []
            
            return filepath
        
        # Clear buffers
        self.redis.delete(episode_key)
        self.current_episode_transitions = []
        
        return None
    
    def get_episode_transitions(
        self,
        goal_id: str,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get transitions for an episode from Redis."""
        episode_key = f"rollout:{goal_id}:transitions"
        transition_jsons = self.redis.lrange(episode_key, 0, limit or -1)
        
        transitions = [json.loads(tj) for tj in transition_jsons]
        transitions.sort(key=lambda t: t.get("timestamp", ""))
        
        return transitions
    
    def export_rollout_dataset(
        self,
        output_path: Path,
        goal_ids: Optional[List[str]] = None,
    ) -> None:
        """
        Export rollout dataset from multiple episodes.
        
        Args:
            output_path: Path to save dataset
            goal_ids: List of goal IDs to export (if None, exports all)
        """
        all_episodes = []
        
        # If goal_ids provided, only export those
        if goal_ids:
            for goal_id in goal_ids:
                episode_key = f"rollout:{goal_id}:transitions"
                transition_jsons = self.redis.lrange(episode_key, 0, -1)
                if transition_jsons:
                    transitions = [json.loads(tj) for tj in transition_jsons]
                    transitions.sort(key=lambda t: t.get("timestamp", ""))
                    all_episodes.append({
                        "goal_id": goal_id,
                        "transitions": transitions,
                    })
        else:
            # Scan for all rollout keys
            cursor = 0
            pattern = "rollout:*:transitions"
            
            while True:
                cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
                for key in keys:
                    # Extract goal_id from key
                    goal_id = key.replace("rollout:", "").replace(":transitions", "")
                    transition_jsons = self.redis.lrange(key, 0, -1)
                    if transition_jsons:
                        transitions = [json.loads(tj) for tj in transition_jsons]
                        transitions.sort(key=lambda t: t.get("timestamp", ""))
                        all_episodes.append({
                            "goal_id": goal_id,
                            "transitions": transitions,
                        })
                
                if cursor == 0:
                    break
        
        # Save dataset
        dataset = {
            "episodes": all_episodes,
            "total_episodes": len(all_episodes),
            "total_transitions": sum(len(ep["transitions"]) for ep in all_episodes),
            "created_at": datetime.utcnow().isoformat(),
        }
        
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, default=str)
        
        print(
            f"[TransitionLogger] Exported {len(all_episodes)} episodes "
            f"({dataset['total_transitions']} transitions) to {output_path}",
            file=sys.stderr
        )

