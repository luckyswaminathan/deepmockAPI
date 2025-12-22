from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

try:
    from dotenv import load_dotenv
    # Load .env from backend directory (parent of scripts/)
    backend_dir = Path(__file__).resolve().parent.parent
    load_dotenv(backend_dir / ".env")
except ImportError:
    pass  # dotenv is optional


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


def _save_snapshot(
    session: requests.Session,
    backend: str,
    episode_id: str,
    state_id: str,
    snapshot_dir: Path,
    step_idx: int,
    action: Optional[dict[str, Any]] = None,
    result: Optional[dict[str, Any]] = None,
) -> None:
    """Persist a full environment snapshot (state + observation) for debugging/training."""
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    state_payload = None
    obs_payload = None
    try:
        state_resp = session.get(f"{backend}/rl/states/{state_id}", timeout=30)
        if state_resp.status_code < 400:
            state_payload = state_resp.json()
    except Exception:
        state_payload = None
    try:
        obs_resp = session.get(f"{backend}/rl/episodes/{episode_id}/observation", timeout=30)
        if obs_resp.status_code < 400:
            obs_payload = obs_resp.json()
    except Exception:
        obs_payload = None
    
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "episode_id": episode_id,
        "step": step_idx,
        "state_id": state_id,
        "state": state_payload,
        "observation": obs_payload,
        "action": action,
        "result": result,
    }
    outfile = snapshot_dir / f"step_{step_idx:03d}.json"
    with outfile.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, default=str)
    print(f"[agent] Snapshot saved to {outfile} (state={state_id})")


def _make_prompt(goal: dict[str, Any], state: dict[str, Any], state_id: str) -> str:
    """Build a training prompt describing goal + current state."""
    goal_desc = goal.get("description") or f"Goal for {goal.get('api_slug')}"
    target = json.dumps(goal.get("goal_state", {}), sort_keys=True)
    modified_components = state.get("modified_components", {}) if isinstance(state, dict) else {}
    current = json.dumps(modified_components, sort_keys=True)
    return (
        f"Goal: {goal_desc}\n"
        f"API: {goal.get('api_slug')}\n"
        f"Target: {target}\n"
        f"CurrentState[{state_id}]: {current}"
    )


def _make_completion(action: dict[str, Any]) -> str:
    """Render an action as a single-line completion string."""
    parts = [str(action.get("method", "")).upper(), action.get("path", "")]
    params = action.get("params") or action.get("query")
    body = action.get("body") or action.get("request_body")
    if params:
        parts.append(f"params={json.dumps(params, sort_keys=True)}")
    if body is not None:
        parts.append(f"body={json.dumps(body, sort_keys=True)}")
    return " ".join(p for p in parts if p)


def _export_episode_datasets(
    session: requests.Session,
    backend: str,
    goal: dict[str, Any],
    episode_id: str,
    executed_steps: list[dict[str, Any]],
    state_history: list[str],
    *,
    output_dir: Path,
    sft_file: str,
    ppo_file: str,
    skip_sft: bool,
    skip_ppo: bool,
    sft_min_reward: float,
    sft_done_only: bool,
) -> tuple[Optional[Path], Optional[Path]]:
    """Build SFT + PPO datasets from the steps we just executed."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sft_path = output_dir / sft_file
    ppo_path = output_dir / ppo_file
    sft_handle = None
    ppo_handle = None
    sft_written = 0
    ppo_written = 0
    try:
        if not skip_sft:
            # Append to accumulate examples across multiple runs
            sft_handle = sft_path.open("a", encoding="utf-8")
        if not skip_ppo:
            # Append to accumulate examples across multiple runs
            ppo_handle = ppo_path.open("a", encoding="utf-8")
    except OSError as exc:
        print(f"[agent] Failed to open dataset files: {exc}", file=sys.stderr)
        return None, None
    
    try:
        for idx, step in enumerate(executed_steps):
            action = step["action"]
            result = step["result"] or {}
            state_id = state_history[idx] if idx < len(state_history) else step.get("state_id")
            next_state_id = step.get("next_state_id") or state_history[idx + 1] if idx + 1 < len(state_history) else None
            reward = result.get("reward", 0.0)
            done = bool(result.get("done"))
            
            state_payload = {}
            if state_id:
                try:
                    resp = session.get(f"{backend}/rl/states/{state_id}", timeout=30)
                    if resp.status_code < 400:
                        state_payload = resp.json()
                except Exception:
                    state_payload = {}
            
            prompt = _make_prompt(goal, state_payload, state_id or "unknown")
            completion = _make_completion(action)
            
            if ppo_handle:
                ppo_payload: Dict[str, Any] = {
                    "prompt": prompt,
                    "completion": completion,
                    "reward": reward,
                    "done": done,
                    "episode_id": episode_id,
                    "goal_id": goal.get("goal_id"),
                    "state_id": state_id,
                    "next_state_id": next_state_id,
                    "response_status": result.get("response_status"),
                    "reason": result.get("reason"),
                    "timestamp": datetime.now(UTC).isoformat(),
                }
                response_body = result.get("response_body")
                if response_body is not None:
                    ppo_payload["response_body"] = response_body
                ppo_handle.write(json.dumps(ppo_payload))
                ppo_handle.write("\n")
                ppo_written += 1
            
            if sft_handle:
                keep = done if sft_done_only else (done or reward >= sft_min_reward)
                if keep:
                    sft_payload = {
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are DeepMock, an API-native agent. Respond with exactly one HTTP request (method, path, optional params/body) that moves the environment toward the goal.",
                            },
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": completion},
                        ],
                    }
                    sft_handle.write(json.dumps(sft_payload))
                    sft_handle.write("\n")
                    sft_written += 1
        
        if sft_handle:
            print(f"[agent] Wrote {sft_written} SFT rows -> {sft_path}")
        if ppo_handle:
            print(f"[agent] Wrote {ppo_written} PPO rows -> {ppo_path}")
        return (sft_path if sft_handle else None, ppo_path if ppo_handle else None)
    finally:
        if sft_handle:
            sft_handle.close()
        if ppo_handle:
            ppo_handle.close()


def _kickoff_openai_jobs(
    sft_path: Optional[Path],
    ppo_path: Optional[Path],
    *,
    api_key: Optional[str],
    api_base: str,
    sft_model: str,
    ppo_model: Optional[str],
    ppo_algorithm: str,
    sft_suffix: Optional[str],
    dry_run: bool,
) -> None:
    """Upload datasets and start OpenAI SFT/PPO jobs using the existing helper."""
    try:
        import push_finetune  # type: ignore
    except ImportError as exc:  # pragma: no cover - convenience path
        print(f"[agent] Cannot import push_finetune helper: {exc}", file=sys.stderr)
        return
    
    if not sft_path and not ppo_path:
        print("[agent] Nothing to upload (no datasets written)")
        return
    if ppo_path and not ppo_model and not sft_path:
        print("[agent] --ppo-model is required when uploading a PPO dataset without an SFT job.", file=sys.stderr)
        return
    
    cli_args: List[str] = []
    if sft_path:
        cli_args.extend(["--sft-file", str(sft_path), "--sft-model", sft_model])
    if sft_suffix:
        cli_args.extend(["--sft-suffix", sft_suffix])
    if ppo_path:
        cli_args.extend(["--ppo-file", str(ppo_path)])
        if ppo_model:
            cli_args.extend(["--ppo-model", ppo_model])
        if ppo_algorithm and ppo_algorithm != "ppo":
            cli_args.extend(["--ppo-algorithm", ppo_algorithm])
    if api_base and api_base != "https://api.openai.com":
        cli_args.extend(["--api-base", api_base])
    if api_key:
        cli_args.extend(["--api-key", api_key])
    if dry_run:
        cli_args.append("--dry-run")
    
    # push_finetune will validate the args (e.g., PPO requires a model id)
    print(f"[agent] Launching training jobs via push_finetune with args: {cli_args}")
    push_finetune.main(cli_args)


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
    parser.add_argument(
        "--snapshot-dir",
        type=Path,
        help="Directory to write per-step environment snapshots (state + observation).",
    )
    parser.add_argument(
        "--export-datasets",
        action="store_true",
        help="Export SFT/PPO datasets from this run using the recorded transitions.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("generated_output/datasets"),
        help="Directory where datasets will be written when --export-datasets is set.",
    )
    parser.add_argument("--sft-file", default="sft.jsonl", help="SFT dataset filename (relative to dataset dir).")
    parser.add_argument("--ppo-file", default="ppo.jsonl", help="PPO dataset filename (relative to dataset dir).")
    parser.add_argument("--skip-sft", action="store_true", help="Skip writing the SFT dataset.")
    parser.add_argument("--skip-ppo", action="store_true", help="Skip writing the PPO dataset.")
    parser.add_argument(
        "--sft-min-reward",
        type=float,
        default=0.0,
        help="Minimum reward required to include a step in the SFT dataset (unless done). Default: 0.0 (include all).",
    )
    parser.add_argument(
        "--sft-done-only",
        action="store_true",
        help="Only include terminal steps in the SFT dataset.",
    )
    parser.add_argument(
        "--push-finetune",
        action="store_true",
        help="Upload the generated datasets to OpenAI and start SFT/PPO training jobs.",
    )
    parser.add_argument("--sft-model", default="gpt-4.1-mini", help="Base model for SFT.")
    parser.add_argument("--sft-suffix", help="Optional suffix when creating the SFT model.")
    parser.add_argument(
        "--ppo-model",
        help="Model to continue RL fine-tuning (defaults to the SFT result when provided).",
    )
    parser.add_argument("--ppo-algorithm", default="ppo", help="RL algorithm name passed to the training API.")
    parser.add_argument("--openai-api-base", default="https://api.openai.com", help="OpenAI API base URL.")
    parser.add_argument("--openai-api-key", help="OpenAI API key (defaults to OPENAI_API_KEY env).")
    parser.add_argument(
        "--dry-run-finetune",
        action="store_true",
        help="Print OpenAI upload/training steps without making API calls.",
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
        resp = session.get(f"{backend}/rl/goals/{goal_id}", timeout=30)
        resp.raise_for_status()
        goal = resp.json()

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
    
    if args.snapshot_dir:
        _save_snapshot(
            session,
            backend,
            episode_id,
            episode["current_state_id"],
            args.snapshot_dir,
            step_idx=0,
            action=None,
            result={"note": "start"},
        )

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
    executed_steps: list[dict[str, Any]] = []

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
        next_state_id = result.get("next_state_id") or state_history[-1]
        state_history.append(next_state_id)  # Track state history
        prev_state_id = state_history[-2] if len(state_history) >= 2 else episode["current_state_id"]
        executed_steps.append(
            {
                "action": action,
                "result": result,
                "state_id": prev_state_id,
                "next_state_id": next_state_id,
            }
        )
        
        if args.snapshot_dir:
            _save_snapshot(
                session,
                backend,
                episode_id,
                next_state_id,
                args.snapshot_dir,
                step_idx=idx,
                action=action,
                result=result,
            )
        
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

    # Build datasets from the collected transitions
    sft_path: Optional[Path] = None
    ppo_path: Optional[Path] = None
    if args.export_datasets:
        if not executed_steps:
            print("[agent] No executed steps recorded; skipping dataset export.")
        else:
            sft_path, ppo_path = _export_episode_datasets(
                session,
                backend,
                goal,
                episode_id,
                executed_steps,
                state_history,
                output_dir=args.dataset_dir,
                sft_file=args.sft_file,
                ppo_file=args.ppo_file,
                skip_sft=args.skip_sft,
                skip_ppo=args.skip_ppo,
                sft_min_reward=args.sft_min_reward,
                sft_done_only=args.sft_done_only,
            )
    
    if args.push_finetune:
        api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[agent] OPENAI_API_KEY (or --openai-api-key) is required for --push-finetune", file=sys.stderr)
        else:
            _kickoff_openai_jobs(
                sft_path,
                ppo_path,
                api_key=api_key,
                api_base=args.openai_api_base,
                sft_model=args.sft_model,
                ppo_model=args.ppo_model,
                ppo_algorithm=args.ppo_algorithm,
                sft_suffix=args.sft_suffix,
                dry_run=args.dry_run_finetune,
            )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
