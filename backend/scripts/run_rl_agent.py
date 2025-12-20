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


def _extract_actions_from_openapi_spec(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract actions (method/path combinations) from an OpenAPI spec.
    
    Only includes mutating operations: POST, PUT, PATCH, DELETE.
    Excludes GET (read-only) since those don't modify state.
    """
    actions = []
    paths = spec.get("paths", {})
    # Only include mutating operations (exclude GET, OPTIONS, HEAD)
    mutating_methods = {"post", "put", "patch", "delete"}
    
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        
        # Skip paths with placeholders (need existing resources)
        if "{" in path:
            continue
        
        for method, operation in path_item.items():
            if method.lower() not in mutating_methods:
                continue
            if not isinstance(operation, dict):
                continue
            
            # Create a basic action
            action = {
                "method": method.upper(),
                "path": path,
            }
            
            # Add minimal body for POST/PUT/PATCH if requestBody exists
            if method.lower() in {"post", "put", "patch"}:
                request_body = operation.get("requestBody")
                if request_body:
                    # Try to extract example or create empty body
                    content = request_body.get("content", {})
                    json_content = content.get("application/json") or content.get("application/*+json")
                    if json_content:
                        schema = json_content.get("schema", {})
                        example = json_content.get("example") or schema.get("example")
                        if example:
                            action["body"] = example
                        else:
                            # Create minimal body based on required fields
                            required = schema.get("required", [])
                            properties = schema.get("properties", {})
                            body = {}
                            for prop_name in required[:3]:  # Limit to first 3 required fields
                                prop_schema = properties.get(prop_name, {})
                                prop_type = prop_schema.get("type", "string")
                                if prop_type == "string":
                                    body[prop_name] = f"example_{prop_name}"
                                elif prop_type == "number" or prop_type == "integer":
                                    body[prop_name] = 0
                                elif prop_type == "boolean":
                                    body[prop_name] = False
                            if body:
                                action["body"] = body
            
            actions.append(action)
    
    return actions


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
    parser.add_argument("--max-actions", type=int, default=100, help="Maximum number of actions to execute (0 = unlimited)")
    parser.add_argument(
        "--reset-to-step",
        type=int,
        help="Reset episode to state at step N (1-indexed) before executing actions",
    )
    parser.add_argument(
        "--reset-to-state",
        type=str,
        help="Reset episode to specific state_id before executing actions",
    )
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

    actions_data = _load_json(args.actions_file)
    
    # Check if it's an OpenAPI spec and convert it
    if isinstance(actions_data, dict):
        if "openapi" in actions_data or "swagger" in actions_data or "paths" in actions_data:
            print(f"[agent] Detected OpenAPI spec, extracting paths...")
            actions = _extract_actions_from_openapi_spec(actions_data)
            print(f"[agent] Extracted {len(actions)} actions from OpenAPI spec")
        else:
            raise SystemExit(
                f"Error: Actions file must contain a JSON array (list) or OpenAPI spec.\n"
                f"Expected format: [{{'method': 'POST', 'path': '/v1/customers'}}, ...] or OpenAPI spec\n"
                f"Got: {type(actions_data).__name__} with keys: {list(actions_data.keys())[:5]}..."
            )
    elif isinstance(actions_data, list):
        actions = actions_data
    else:
        raise SystemExit(
            f"Error: Actions file must contain a JSON array (list) or OpenAPI spec, but got {type(actions_data).__name__}.\n"
            f"Expected format: [{{'method': 'POST', 'path': '/v1/customers', 'body': {{...}}}}, ...]"
        )
    
    print(f"[agent] Loaded {len(actions)} actions from {args.actions_file}")

    # Reset to specific step or state if requested
    if args.reset_to_step or args.reset_to_state:
        # First, we need to execute actions up to the reset point to get the state
        if args.reset_to_step:
            if args.reset_to_step < 1:
                raise SystemExit("--reset-to-step must be >= 1")
            if args.reset_to_step > len(actions):
                raise SystemExit(f"--reset-to-step {args.reset_to_step} exceeds available actions ({len(actions)})")
            
            print(f"[agent] Executing first {args.reset_to_step} actions to reach reset point...")
            reset_state_id = None
            for idx, action in enumerate(actions[: args.reset_to_step], start=1):
                print(f"[agent] Step {idx}: {action.get('method')} {action.get('path')}")
                resp = session.post(
                    f"{backend}/rl/episodes/{episode_id}/actions",
                    json=action,
                    timeout=60,
                )
                if resp.status_code >= 400:
                    print(f"[agent] Action failed: {resp.status_code} {resp.text.strip()}")
                    raise SystemExit(f"Failed to reach reset point at step {args.reset_to_step}")
                result = resp.json()
                reset_state_id = result.get("next_state_id")
                if result.get("done"):
                    print("[agent] Goal reached before reset point")
                    break
            
            if not reset_state_id:
                # Get current episode state
                resp = session.get(f"{backend}/rl/episodes/{episode_id}")
                resp.raise_for_status()
                episode_data = resp.json()
                reset_state_id = episode_data.get("current_state_id")
            
            print(f"[agent] Resetting to state at step {args.reset_to_step}: {reset_state_id}")
        else:
            reset_state_id = args.reset_to_state
            print(f"[agent] Resetting to state: {reset_state_id}")
        
        # Reset episode to that state
        resp = session.post(
            f"{backend}/rl/episodes/{episode_id}/reset",
            json={"state_id": reset_state_id},
            timeout=30,
        )
        resp.raise_for_status()
        reset_result = resp.json()
        print(f"[agent] Reset complete: {reset_result.get('message')}")
        
        # Get updated episode
        resp = session.get(f"{backend}/rl/episodes/{episode_id}")
        resp.raise_for_status()
        episode = resp.json()
        print(f"[agent] Continuing from state: {episode['current_state_id']}")

    # Apply max_actions limit if set (0 means unlimited)
    # If we reset, start from the reset point
    start_idx = args.reset_to_step if args.reset_to_step else 0
    actions_to_execute = actions[start_idx:]
    if args.max_actions > 0:
        actions_to_execute = actions_to_execute[: args.max_actions]
    
    print(f"[agent] Executing {len(actions_to_execute)} actions (starting from step {start_idx + 1})")
    
    # Track state history for potential resets
    state_history = [episode['current_state_id']]  # Start with current state
    
    for idx, action in enumerate(actions_to_execute, start=start_idx + 1):
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
        next_state_id = result.get("next_state_id")
        state_history.append(next_state_id)  # Track state history
        
        # Get state details for debugging
        try:
            resp_state = session.get(f"{backend}/rl/states/{next_state_id}")
            if resp_state.status_code == 200:
                state_data = resp_state.json()
                parent_state_id = state_data.get("parent_state_id", "None")
                components = state_data.get("modified_components", {})
                component_names = list(components.keys()) if components else []
                print(
                    "    -> reward={reward:.3f} done={done} next_state={next_state_id} parent={parent} "
                    "components={comps} status={status} (state_history: {step})".format(
                        reward=result.get("reward", 0.0),
                        done=result.get("done", False),
                        next_state_id=next_state_id,
                        parent=parent_state_id,
                        comps=component_names[:3] if component_names else "[]",  # Show first 3 components
                        status=result.get("response_status"),
                        step=len(state_history),
                    )
                )
            else:
                print(
                    "    -> reward={reward:.3f} done={done} next_state={next_state_id} status={status} (state_history: {step})".format(
                        reward=result.get("reward", 0.0),
                        done=result.get("done", False),
                        next_state_id=next_state_id,
                        status=result.get("response_status"),
                        step=len(state_history),
                    )
                )
        except Exception:
            print(
                "    -> reward={reward:.3f} done={done} next_state={next_state_id} status={status} (state_history: {step})".format(
                    reward=result.get("reward", 0.0),
                    done=result.get("done", False),
                    next_state_id=next_state_id,
                    status=result.get("response_status"),
                    step=len(state_history),
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
