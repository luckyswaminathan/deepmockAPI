"""Run a basic RLlib PPO loop against the DeepMockGymEnv."""

from __future__ import annotations

import argparse
import json
import os
import warnings
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import numpy as np

try:
    import gymnasium as gym  # type: ignore
    from gymnasium import spaces  # type: ignore
except ImportError:  # pragma: no cover - fall back to classic gym
    import gym  # type: ignore
    from gym import spaces  # type: ignore

from rl.gym_env import DeepMockGymEnv

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ.setdefault("PYTHONWARNINGS", "ignore::DeprecationWarning")


def _load_json(path: Optional[Path]) -> Optional[dict[str, Any]]:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require_rllib():
    try:
        import ray  # type: ignore
        from ray.rllib.algorithms.algorithm import Algorithm  # type: ignore
        from ray.rllib.algorithms.ppo import PPOConfig  # type: ignore
        from ray.tune.registry import register_env  # type: ignore
    except ImportError as exc:  # pragma: no cover - import guard
        raise SystemExit(
            "Ray RLlib is required for this script. Install it with: pip install \"ray[rllib]\""
        ) from exc
    return ray, Algorithm, PPOConfig, register_env


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train PPO with RLlib against DeepMockGymEnv.")
    parser.add_argument("--backend-url", default=os.getenv("BACKEND_URL", "http://localhost:8000"))
    parser.add_argument("--api-slug", required=True, help="Generated API slug (used for /generated/{slug} routes).")
    parser.add_argument(
        "--goal-file",
        type=Path,
        help="JSON payload for creating a goal (same shape as POST /rl/goals). Required unless --goal-id is set.",
    )
    parser.add_argument("--goal-id", help="Reuse an existing goal id instead of creating one.")
    parser.add_argument(
        "--actions-file",
        type=Path,
        help="Optional JSON list of actions to use instead of discovering from OpenAPI.",
    )
    parser.add_argument("--openapi-path", default="/openapi.json", help="OpenAPI path used for action discovery.")
    parser.add_argument("--num-iterations", type=int, default=3, help="Number of PPO training iterations to run.")
    parser.add_argument("--num-workers", type=int, default=0, help="Ray rollout workers (0 runs everything locally).")
    parser.add_argument("--rollout-fragment-length", type=int, default=200, help="Timesteps per rollout fragment.")
    parser.add_argument("--train-batch-size", type=int, default=4000, help="Collected batch size per training step.")
    parser.add_argument("--sgd-minibatch-size", type=int, default=256, help="SGD minibatch size for PPO.")
    parser.add_argument("--lr", type=float, default=5e-4, help="Learning rate for PPO.")
    parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor for future rewards.")
    parser.add_argument("--framework", choices=["torch", "tf2"], default="torch", help="Deep learning backend for RLlib.")
    parser.add_argument("--max-steps", type=int, help="Max steps per episode before truncation.")
    parser.add_argument(
        "--invalid-action-penalty",
        type=float,
        default=-1.0,
        help="Reward applied when an invalid action is attempted.",
    )
    parser.add_argument(
        "--disable-action-mask",
        action="store_true",
        help="Skip /valid-actions calls (helps when backend does not expose the mask).",
    )
    parser.add_argument(
        "--allow-invalid-actions",
        action="store_true",
        help="Do not short-circuit invalid actions even when the mask is enabled.",
    )
    parser.add_argument(
        "--evaluation-episodes",
        type=int,
        default=2,
        help="Episodes to run during evaluation. Set to 0 to disable evaluation.",
    )
    parser.add_argument(
        "--evaluation-interval",
        type=int,
        default=1,
        help="How often to run evaluation (in training iterations).",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=Path("rllib_checkpoints"),
        help="Directory to write checkpoints into.",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=1,
        help="Save a checkpoint every N iterations (also saves the final one).",
    )
    parser.add_argument(
        "--vectorize-observation",
        dest="vectorize_observation",
        action="store_true",
        default=True,
        help="Convert dict/sequence observations into a fixed-length vector for RLlib (recommended).",
    )
    parser.add_argument(
        "--no-vectorize-observation",
        dest="vectorize_observation",
        action="store_false",
        help="Disable observation vectorization (may fail with complex observation spaces).",
    )

    args = parser.parse_args(argv)
    if not args.goal_id and not args.goal_file:
        parser.error("Provide either --goal-id or --goal-file so the environment can start a goal/episode.")
    if args.evaluation_episodes < 0:
        parser.error("--evaluation-episodes must be >= 0")
    if args.evaluation_interval < 1:
        parser.error("--evaluation-interval must be >= 1")
    return args


def _build_env_config(args: argparse.Namespace) -> Dict[str, Any]:
    goal = _load_json(args.goal_file)
    actions = _load_json(args.actions_file)
    env_config = {
        "backend_url": args.backend_url,
        "api_slug": args.api_slug,
        "goal": goal,
        "goal_id": args.goal_id,
        "actions": actions,
        "openapi_path": args.openapi_path,
        "use_action_mask": not args.disable_action_mask,
        "enforce_valid_actions": not args.allow_invalid_actions,
        "invalid_action_penalty": args.invalid_action_penalty,
        "max_steps": args.max_steps,
    }
    return {k: v for k, v in env_config.items() if v is not None}


class VectorizedObservationEnv(gym.ObservationWrapper):
    """Convert DeepMockGymEnv observations into a fixed-length Box for RLlib."""

    def __init__(self, env: gym.Env):
        super().__init__(env)
        components = getattr(env, "components", []) or []
        self.components: list[str] = list(components)
        base_features = 7  # required, satisfied, last_k, steps_remaining, last_status, last_action_id_len, known_id_total
        component_features = 3 * len(self.components)  # per component: required?, satisfied?, known_id_count
        feature_len = base_features + component_features
        self.observation_space = spaces.Box(low=-1e6, high=1e6, shape=(feature_len,), dtype=np.float32)

    def observation(self, obs: Dict[str, Any]) -> np.ndarray:
        required = obs.get("required") or []
        satisfied = obs.get("satisfied") or []
        last_k = obs.get("last_k_components") or []
        known_ids = obs.get("known_ids") or {}
        last_status = obs.get("last_status", -1) or -1
        last_action_id = obs.get("last_action_id") or ""

        features: list[float] = [
            float(len(required)),
            float(len(satisfied)),
            float(len(last_k)),
            float(obs.get("steps_remaining", 0) or 0),
            float(last_status),
            float(len(str(last_action_id))),
            float(sum(len(v) for v in known_ids.values() if isinstance(v, (list, tuple)))),
        ]

        for component in self.components:
            features.append(1.0 if component in required else 0.0)
            features.append(1.0 if component in satisfied else 0.0)
            count = known_ids.get(component) or []
            features.append(float(len(count)) if isinstance(count, (list, tuple)) else 0.0)

        return np.array(features, dtype=np.float32)


def _print_result(iteration: int, metrics: Mapping[str, Any]) -> None:
    reward_mean = metrics.get("episode_reward_mean")
    length_mean = metrics.get("episode_len_mean")
    timesteps_total = metrics.get("timesteps_total")
    fmt_reward = f"{reward_mean:.3f}" if isinstance(reward_mean, (int, float)) else "n/a"
    fmt_len = f"{length_mean:.1f}" if isinstance(length_mean, (int, float)) else "n/a"
    print(f"[train] iter={iteration} reward_mean={fmt_reward} len_mean={fmt_len} timesteps={timesteps_total}")

    eval_metrics = metrics.get("evaluation_metrics") or {}
    if eval_metrics:
        eval_reward = eval_metrics.get("episode_reward_mean")
        eval_len = eval_metrics.get("episode_len_mean")
        fmt_eval_reward = f"{eval_reward:.3f}" if isinstance(eval_reward, (int, float)) else "n/a"
        fmt_eval_len = f"{eval_len:.1f}" if isinstance(eval_len, (int, float)) else "n/a"
        print(f"[eval ] reward_mean={fmt_eval_reward} len_mean={fmt_eval_len}")


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    env_config = _build_env_config(args)
    ray, Algorithm, PPOConfig, register_env = _require_rllib()

    def _env_creator(config: Dict[str, Any]) -> gym.Env:
        merged = dict(env_config)
        merged.update(config or {})
        base_env = DeepMockGymEnv(**merged)
        if args.vectorize_observation:
            return VectorizedObservationEnv(base_env)
        return base_env

    register_env("deepmock-gym", _env_creator)

    # Print observation and action spaces
    test_env = _env_creator({})
    print("OBS SPACE:", test_env.observation_space)
    print("ACT SPACE:", test_env.action_space)
    test_env.close()

    config = PPOConfig().environment(env="deepmock-gym", env_config=env_config, disable_env_checking=True)
    config = config.framework(args.framework)
    # Disable new API stack to avoid encoder configuration issues with complex observation spaces
    config = config.api_stack(
        enable_rl_module_and_learner=False,
        enable_env_runner_and_connector_v2=False,
    )

    # RLlib 2.30+ renamed rollouts() to env_runners(); keep backward compatibility.
    if hasattr(config, "env_runners"):
        config = config.env_runners(
            num_env_runners=args.num_workers,
            rollout_fragment_length=args.rollout_fragment_length,
            batch_mode="complete_episodes",
        )
    else:  # pragma: no cover - fallback for older RLlib
        config = config.rollouts(
            num_rollout_workers=args.num_workers,
            rollout_fragment_length=args.rollout_fragment_length,
            batch_mode="complete_episodes",
        )

    config = config.training(
        lr=args.lr,
        gamma=args.gamma,
        model={
            "fcnet_hiddens": [256, 256],
            "fcnet_activation": "tanh",
        },
    )
    # Set batch sizes on the config to satisfy both old and new RLlib field names.
    config.train_batch_size = args.train_batch_size
    config.sgd_minibatch_size = args.sgd_minibatch_size
    if hasattr(config, "minibatch_size"):
        config.minibatch_size = args.sgd_minibatch_size

    if args.evaluation_episodes > 0:
        eval_kwargs: Dict[str, Any] = {
            "evaluation_interval": args.evaluation_interval,
            "evaluation_duration": args.evaluation_episodes,
            "evaluation_duration_unit": "episodes",
            "evaluation_config": {"explore": False},
        }
        if hasattr(config, "evaluation_num_env_runners"):
            eval_kwargs["evaluation_num_env_runners"] = 1
        else:  # pragma: no cover - fallback for older RLlib
            eval_kwargs["evaluation_num_rollout_workers"] = 1
        config = config.evaluation(**eval_kwargs)

    algo: Optional[Algorithm] = None
    try:
        ray.init(ignore_reinit_error=True)
        algo = config.build()
        args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        for iteration in range(1, args.num_iterations + 1):
            result = algo.train()
            _print_result(iteration, result)

            should_checkpoint = iteration % args.checkpoint_interval == 0 or iteration == args.num_iterations
            if should_checkpoint:
                checkpoint = algo.save(checkpoint_dir=str(args.checkpoint_dir))
                ckpt_path = getattr(checkpoint, "path", None)
                if ckpt_path is None and hasattr(checkpoint, "to_directory"):
                    ckpt_path = checkpoint.to_directory()  # type: ignore[call-arg]
                print(f"[checkpoint] saved to {ckpt_path or checkpoint}")
    except KeyboardInterrupt:
        print("Interrupted; shutting down RLlib loop.")
    finally:
        if algo is not None:
            algo.stop()
        ray.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
