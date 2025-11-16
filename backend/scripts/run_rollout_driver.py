"""
Configurable rollout driver that replays scripted HTTP traces against the RL API.

The script expects a YAML or JSON configuration file that lists one or more
scenarios. Each scenario points at an RL goal (either by id or by supplying the
payload the `/rl/goals` endpoint expects) and one or more action sequences to
replay for that goal. Every action element maps directly to
`POST /rl/episodes/{episode_id}/actions` and can include templated strings
rendered via Jinja2 so you can randomize payload fields per episode.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional
from uuid import uuid4

import requests
import yaml
from jinja2 import Environment, StrictUndefined
from requests import Response, Session


def _load_data(path: Path) -> Any:
    """Load YAML or JSON payloads with a single helper."""
    with path.open("r", encoding="utf-8") as handle:
        text = handle.read()
    if path.suffix.lower() in {".json"}:
        return json.loads(text)
    return yaml.safe_load(text)


def _resolve_path(base_dir: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def _ensure_list(value: Any, value_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{value_name} must be a list, got {type(value).__name__}")
    return value


class TemplateRenderer:
    """Simple Jinja2 wrapper with helper functions exposed to templates."""

    def __init__(self) -> None:
        self.env = Environment(autoescape=False, undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        self.env.globals.update(
            uuid4=lambda: uuid4().hex,
            randrange=lambda start=0, stop=10_000: random.randrange(int(start), int(stop)),
            randint=lambda start=0, stop=10_000: random.randint(int(start), int(stop)),
            uniform=lambda start=0.0, stop=1.0: random.uniform(float(start), float(stop)),
            choice=lambda seq: random.choice(list(seq)),
            now_iso=lambda: datetime.utcnow().isoformat(),
            env=os.environ,
        )

    def render(self, value: Any, context: Mapping[str, Any]) -> Any:
        """Recursively render templates inside nested data structures."""
        if isinstance(value, str):
            if "{{" in value or "{%" in value:
                template = self.env.from_string(value)
                return template.render(**context)
            return value
        if isinstance(value, list):
            return [self.render(item, context) for item in value]
        if isinstance(value, dict):
            return {key: self.render(val, context) for key, val in value.items()}
        return value


@dataclass
class ActionSequence:
    """Represents a single action sequence to replay."""

    name: str
    actions: list[dict[str, Any]]
    repetitions: int
    max_actions: Optional[int] = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch rollout driver for RL goals.")
    parser.add_argument("--config", type=Path, required=True, help="YAML/JSON file describing rollout scenarios.")
    parser.add_argument("--backend-url", help="Override backend URL instead of using the config default.")
    parser.add_argument("--only", action="append", help="Scenario name to run (repeatable). Runs every scenario when omitted.")
    parser.add_argument("--dry-run", action="store_true", help="Render actions and print them without executing HTTP calls.")
    parser.add_argument("--max-actions", type=int, help="Global guardrail for how many actions are allowed per episode.")
    return parser.parse_args(argv)


def _load_actions_from_spec(spec: Mapping[str, Any], base_dir: Path) -> list[dict[str, Any]]:
    if "actions" in spec:
        return _ensure_list(spec["actions"], "actions")
    if "actions_file" in spec:
        path = _resolve_path(base_dir, spec["actions_file"])
        data = _load_data(path)
        return _ensure_list(data, f"actions file {path}")
    raise ValueError("Each sequence requires either inline `actions` or an `actions_file` reference.")


def _expand_sequences(
    scenario: Mapping[str, Any],
    base_dir: Path,
) -> list[ActionSequence]:
    sequences: list[ActionSequence] = []
    default_repeat = int(scenario.get("episodes", 1))
    default_max_actions = scenario.get("max_actions")

    if "action_sequences" in scenario:
        for idx, seq in enumerate(_ensure_list(scenario["action_sequences"], "action_sequences"), start=1):
            name = seq.get("name") or f"{scenario.get('name', 'scenario')}-seq{idx}"
            actions = _load_actions_from_spec(seq, base_dir)
            repetitions = int(seq.get("repetitions") or seq.get("episodes") or default_repeat)
            max_actions = seq.get("max_actions", default_max_actions)
            sequences.append(ActionSequence(name=name, actions=actions, repetitions=repetitions, max_actions=max_actions))
    else:
        actions = _load_actions_from_spec(scenario, base_dir)
        sequences.append(
            ActionSequence(
                name=scenario.get("name", "default"),
                actions=actions,
                repetitions=default_repeat,
                max_actions=default_max_actions,
            )
        )
    return sequences


def _create_goal(session: Session, backend: str, scenario: Mapping[str, Any], base_dir: Path) -> str:
    payload: Optional[dict[str, Any]] = None
    if scenario.get("goal_id"):
        return str(scenario["goal_id"])
    if scenario.get("goal_file"):
        goal_path = _resolve_path(base_dir, scenario["goal_file"])
        payload = _load_data(goal_path)
        if not isinstance(payload, dict):
            raise ValueError(f"Goal file {goal_path} must contain an object payload.")
    elif scenario.get("goal"):
        payload = scenario["goal"]
    if not payload:
        raise ValueError(f"Scenario {scenario.get('name')} must specify `goal_id`, `goal`, or `goal_file`.")

    resp = session.post(f"{backend}/rl/goals", json=payload, timeout=30)
    resp.raise_for_status()
    goal = resp.json()
    goal_id = goal["goal_id"]
    print(f"[driver] Created goal {goal_id} for API {goal.get('api_slug')}")
    return goal_id


def _start_episode(session: Session, backend: str, goal_id: str) -> dict[str, Any]:
    resp = session.post(f"{backend}/rl/goals/{goal_id}/episodes", json={"goal_id": goal_id}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _execute_action(
    session: Session,
    backend: str,
    episode_id: str,
    action_payload: Mapping[str, Any],
) -> Response:
    return session.post(
        f"{backend}/rl/episodes/{episode_id}/actions",
        json=action_payload,
        timeout=60,
    )


def _build_context(
    scenario: Mapping[str, Any],
    goal_id: str,
    sequence_name: str,
    repetition_index: int,
    step_index: int,
    response_memory: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "scenario": scenario.get("name"),
        "sequence": sequence_name,
        "goal_id": goal_id,
        "episode_iteration": repetition_index,
        "step_index": step_index,
        "history": response_memory,
        "last_response": response_memory[-1] if response_memory else None,
        "vars": scenario.get("vars", {}),
        "run_id": os.getenv("ROLL_OUT_RUN_ID") or uuid4().hex[:8],
    }


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = args.config.resolve()
    config = _load_data(config_path)
    if not isinstance(config, dict):
        raise SystemExit("Config root must be an object with `scenarios`.")

    scenarios = _ensure_list(config.get("scenarios"), "scenarios")
    backend_default = args.backend_url or config.get("backend_url") or "http://localhost:8000"
    renderer = TemplateRenderer()
    session = requests.Session()
    base_dir = config_path.parent
    selected = set(args.only) if args.only else None

    for scenario in scenarios:
        name = scenario.get("name")
        if selected and name not in selected:
            continue
        backend = scenario.get("backend_url", backend_default).rstrip("/")
        try:
            goal_id = _create_goal(session, backend, scenario, base_dir)
        except Exception as exc:
            print(f"[driver] Failed to resolve goal for scenario {name}: {exc}", file=sys.stderr)
            continue

        sequences = _expand_sequences(scenario, base_dir)
        headers_default = scenario.get("default_headers") or {}

        print(f"[driver] Running scenario '{name}' ({len(sequences)} sequence(s)) targeting goal {goal_id}")
        for sequence in sequences:
            for repetition in range(sequence.repetitions):
                print(f"[driver]   Episode {repetition + 1}/{sequence.repetitions} for sequence '{sequence.name}'")
                if args.dry_run:
                    episode = {"episode_id": "dry-run", "current_state_id": "<none>"}
                else:
                    try:
                        episode = _start_episode(session, backend, goal_id)
                    except Exception as exc:
                        print(f"[driver]     Failed to start episode: {exc}", file=sys.stderr)
                        break
                episode_id = episode["episode_id"]
                response_memory: list[dict[str, Any]] = []

                for step_index, template_action in enumerate(sequence.actions, start=1):
                    if sequence.max_actions and step_index > sequence.max_actions:
                        print(f"[driver]     Reached sequence max actions ({sequence.max_actions}), stopping.")
                        break
                    if args.max_actions and step_index > args.max_actions:
                        print(f"[driver]     Reached global max actions ({args.max_actions}), stopping.")
                        break

                    context = _build_context(scenario, goal_id, sequence.name, repetition, step_index - 1, response_memory)
                    rendered_action = renderer.render(template_action, context)
                    method = rendered_action.get("method", "GET").upper()
                    path = rendered_action.get("path")
                    if not path:
                        print(f"[driver]     Action missing path at step {step_index}, skipping.")
                        continue
                    params = rendered_action.get("params")
                    body = rendered_action.get("body")
                    headers = {**headers_default, **rendered_action.get("headers", {})}

                    action_payload: dict[str, Any] = {"method": method, "path": path}
                    if params:
                        action_payload["params"] = params
                    if body is not None:
                        action_payload["body"] = body
                    if headers:
                        action_payload["headers"] = headers

                    print(f"[driver]     Step {step_index}: {method} {path}")
                    if args.dry_run:
                        print(f"[driver]       payload={json.dumps(action_payload, indent=2)}")
                        continue

                    resp = _execute_action(session, backend, episode_id, action_payload)
                    if resp.status_code >= 400:
                        print(f"[driver]       Action failed: {resp.status_code} {resp.text.strip()}")
                        break
                    data = resp.json()
                    response_memory.append(data)
                    reward = data.get("reward", 0.0)
                    done = data.get("done", False)
                    next_state = data.get("next_state_id")
                    status = data.get("response_status")
                    print(f"[driver]       -> reward={reward:.3f} done={done} next_state={next_state} status={status}")
                    if done:
                        print("[driver]       Goal reached, finishing episode early.")
                        break
                else:
                    # Completed loop without break
                    continue
                # Episode terminated early or faced an error; continue to next sequence repetition
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(run())
