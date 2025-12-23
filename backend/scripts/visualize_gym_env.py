"""Interactive/CLI visualizer for the DeepMockGymEnv."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from rl.gym_env import DeepMockGymEnv


def _load_json(path: Optional[Path]) -> Optional[dict[str, Any] | list[Any]]:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _print_actions(env: DeepMockGymEnv) -> None:
    print("\nAvailable actions:")
    for idx, action in enumerate(env.actions):
        summary = action.get("summary") or ""
        print(f"  [{idx}] {action['method']:6s} {action['path']} {summary}")


def _summarize_observation(obs: Dict[str, Any]) -> str:
    required = obs.get("required") or []
    satisfied = obs.get("satisfied") or []
    known_ids = obs.get("known_ids") or {}
    last_action_id = obs.get("last_action_id") or ""
    last_status = obs.get("last_status")
    steps_remaining = obs.get("steps_remaining")
    return (
        f"required={required} | satisfied={satisfied} | known_ids={known_ids} | "
        f"last_action_id={last_action_id} | last_status={last_status} | steps_remaining={steps_remaining}"
    )


def _choose_action(env: DeepMockGymEnv, strategy: str, step_idx: int) -> int:
    if strategy == "ordered":
        return step_idx % env.action_space.n
    if strategy == "random":
        return int(env.action_space.sample())

    while True:
        raw = input("Enter action index (or q to quit): ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            raise KeyboardInterrupt
        try:
            action_idx = int(raw)
            if 0 <= action_idx < env.action_space.n:
                return action_idx
            print(f"Please choose between 0 and {env.action_space.n - 1}.")
        except ValueError:
            print("Not a number; try again.")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize DeepMockGymEnv rollouts (Stripe example compatible).")
    parser.add_argument("--backend-url", default="http://localhost:8000", help="Backend base URL.")
    parser.add_argument("--api-slug", required=True, help="Generated API slug (e.g., stripe).")
    parser.add_argument("--goal-file", type=Path, help="Goal JSON payload to POST to /rl/goals.")
    parser.add_argument("--goal-id", help="Existing goal id to reuse.")
    parser.add_argument("--actions-file", type=Path, help="Optional actions JSON list; defaults to OpenAPI discovery.")
    parser.add_argument("--openapi-path", default="/openapi.json", help="OpenAPI path for action discovery.")
    parser.add_argument("--max-steps", type=int, default=10, help="Max steps to run.")
    parser.add_argument(
        "--policy",
        choices=["manual", "ordered", "random"],
        default="manual",
        help="Action selection strategy.",
    )
    parser.add_argument("--disable-action-mask", action="store_true", help="Skip /valid-actions masking.")
    parser.add_argument("--allow-invalid-actions", action="store_true", help="Do not short-circuit invalid actions.")
    parser.add_argument("--invalid-action-penalty", type=float, default=-1.0, help="Penalty for invalid actions.")
    parser.add_argument("--max-steps-per-episode", type=int, help="Truncation cap passed to the env.")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    goal = _load_json(args.goal_file)
    actions = _load_json(args.actions_file)

    env = DeepMockGymEnv(
        backend_url=args.backend_url,
        api_slug=args.api_slug,
        goal=goal if isinstance(goal, dict) else None,
        goal_id=args.goal_id,
        actions=actions if isinstance(actions, list) else None,
        openapi_path=args.openapi_path,
        use_action_mask=not args.disable_action_mask,
        enforce_valid_actions=not args.allow_invalid_actions,
        invalid_action_penalty=args.invalid_action_penalty,
        max_steps=args.max_steps_per_episode,
    )

    print(f"Connected to {args.backend_url} for API slug '{args.api_slug}'")
    _print_actions(env)

    try:
        obs, info = env.reset()
        print(f"\nEpisode started: {info}")
        print(f"Observation: {_summarize_observation(obs)}")

        for step_idx in range(args.max_steps):
            try:
                action_idx = _choose_action(env, args.policy, step_idx)
            except KeyboardInterrupt:
                print("\nStopping visualization.")
                break

            action = env.actions[action_idx]
            print(f"\nStep {step_idx + 1} | action[{action_idx}]: {action['method']} {action['path']}")

            obs, reward, terminated, truncated, step_info = env.step(action_idx)
            print(f"Reward: {reward} | terminated={terminated} truncated={truncated} | info={step_info}")
            print(f"Observation: {_summarize_observation(obs)}")

            if terminated or truncated:
                print("\nEpisode finished; resetting.")
                obs, info = env.reset()
                print(f"New episode: {info}")
                print(f"Observation: {_summarize_observation(obs)}")
    finally:
        env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
