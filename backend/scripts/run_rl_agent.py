from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import requests


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple rollout runner that drives the RL APIs for a goal.",
    )
    parser.add_argument("--backend-url", default="http://localhost:8000", help="FastAPI backend base URL")
    parser.add_argument("--api-slug", help="API slug to target")
    parser.add_argument("--goal-id", help="Existing goal id to reuse")
    parser.add_argument(
        "--goal-file",
        type=Path,
        help="Path to a JSON goal payload (used when --goal-id not supplied)",
    )
    parser.add_argument(
        "--actions-file",
        type=Path,
        required=True,
        help="JSON file describing a list of actions to play (method/path/params/body)",
    )
    parser.add_argument("--max-actions", type=int, default=100, help="Maximum number of actions to execute")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    backend = args.backend_url.rstrip("/")
    session = requests.Session()

    goal_id = args.goal_id
    if not goal_id:
        if not args.goal_file:
            raise SystemExit("--goal-file is required when --goal-id is not provided")
        goal_payload = _load_json(args.goal_file)
        if args.api_slug:
            goal_payload.setdefault("api_slug", args.api_slug)
        print(f"[agent] Creating goal for API {goal_payload.get('api_slug')}")
        resp = session.post(f"{backend}/rl/goals", json=goal_payload, timeout=30)
        resp.raise_for_status()
        goal = resp.json()
        goal_id = goal["goal_id"]
    else:
        print(f"[agent] Reusing goal {goal_id}")

    print(f"[agent] Starting episode for goal {goal_id}")
    resp = session.post(
        f"{backend}/rl/goals/{goal_id}/episodes",
        json={"goal_id": goal_id},
        timeout=30,
    )
    resp.raise_for_status()
    episode = resp.json()
    episode_id = episode["episode_id"]
    print(f"[agent] Episode {episode_id} started at state {episode['current_state_id']}")

    actions = _load_json(args.actions_file)
    if not isinstance(actions, list):
        raise SystemExit("Actions file must contain a JSON list")

    for idx, action in enumerate(actions[: args.max_actions], start=1):
        print(f"[agent] Step {idx}: {action.get('method')} {action.get('path')}")
        resp = session.post(
            f"{backend}/rl/episodes/{episode_id}/actions",
            json=action,
            timeout=60,
        )
        if resp.status_code >= 400:
            print(f"[agent] Action failed: {resp.status_code} {resp.text.strip()}")
            break
        result = resp.json()
        print(
            "    -> reward={reward:.3f} done={done} next_state={next_state_id} status={status}".format(
                reward=result.get("reward", 0.0),
                done=result.get("done", False),
                next_state_id=result.get("next_state_id"),
                status=result.get("response_status"),
            )
        )
        if result.get("done"):
            print("[agent] Goal reached, stopping early")
            break
    else:
        print("[agent] Reached max actions without finishing goal")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
