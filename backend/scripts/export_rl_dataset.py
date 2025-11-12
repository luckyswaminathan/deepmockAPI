"""Export RL rollouts into JSONL datasets for SFT and PPO fine-tuning."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from rl.action_tracker import ActionTracker
from rl.goal_manager import GoalManager
from rl.models import Episode
from rl.redis_client import get_redis_client
from rl.reward_calculator import RewardCalculator
from rl.state_manager import StateManager
from rl.utils import json_to_model


SYSTEM_PROMPT = (
    "You are DeepMock, an API-native agent. Respond with exactly one HTTP request "
    "(method, path, optional params/body) that moves the environment toward the goal."
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export recorded RL episodes to SFT and PPO JSONL files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated_output/datasets"),
        help="Directory where JSONL files will be written.",
    )
    parser.add_argument(
        "--sft-file",
        default="sft.jsonl",
        help="Filename for the supervised fine-tuning dataset (relative to output dir).",
    )
    parser.add_argument(
        "--ppo-file",
        default="ppo.jsonl",
        help="Filename for the PPO / RL dataset (relative to output dir).",
    )
    parser.add_argument(
        "--skip-sft",
        action="store_true",
        help="Do not emit an SFT dataset.",
    )
    parser.add_argument(
        "--skip-ppo",
        action="store_true",
        help="Do not emit a PPO dataset.",
    )
    parser.add_argument(
        "--sft-min-reward",
        type=float,
        default=0.7,
        help="Minimum reward for a transition to be kept in the SFT file (done states always included).",
    )
    parser.add_argument(
        "--done-only",
        action="store_true",
        help="Only include transitions that finished the goal in the SFT dataset.",
    )
    parser.add_argument(
        "--episode-id",
        action="append",
        dest="episode_ids",
        default=[],
        help="Explicit episode_id to export (can be provided multiple times).",
    )
    parser.add_argument(
        "--episodes-file",
        type=Path,
        help="Path to a JSON/line-delimited file containing episode_ids to export.",
    )
    parser.add_argument(
        "--goal-id",
        help="If provided, only export episodes created for this goal.",
    )
    parser.add_argument(
        "--max-episodes",
        type=int,
        help="Optional cap on the number of episodes to export (after filtering).",
    )
    parser.add_argument(
        "--discover-all",
        action="store_true",
        help="Scan Redis for every stored episode when no episode ids are supplied.",
    )
    return parser.parse_args(argv)


def _load_episode_ids(args: argparse.Namespace) -> list[str]:
    provided: list[str] = list(args.episode_ids or [])
    if args.episodes_file:
        text = args.episodes_file.read_text(encoding="utf-8").strip()
        if not text:
            pass
        else:
            try:
                data = json.loads(text)
                if isinstance(data, list):
                    provided.extend(str(item) for item in data)
                else:
                    raise ValueError
            except ValueError:
                # Treat as newline-delimited plain text
                provided.extend(line.strip() for line in text.splitlines() if line.strip())
    return list(dict.fromkeys(provided))  # preserve order, drop dups


def _discover_episode_ids(redis_client, include_existing: bool) -> Iterable[str]:
    if not include_existing:
        return []
    return (
        key.split(":", 1)[1]
        for key in redis_client.scan_iter("episode:*")
    )


def _serialize_components(components: dict[str, list[dict[str, Any]]]) -> str:
    return json.dumps(components, sort_keys=True)


def _make_prompt(goal, state, state_id: str) -> str:
    goal_desc = goal.description or f"Goal for {goal.api_slug}"
    target = json.dumps(goal.goal_state, sort_keys=True)
    current = _serialize_components(state.modified_components)
    return (
        f"Goal: {goal_desc}\n"
        f"API: {goal.api_slug}\n"
        f"Target: {target}\n"
        f"CurrentState[{state_id}]: {current}"
    )


def _make_completion(action) -> str:
    parts = [action.method.upper(), action.path]
    if action.params:
        parts.append(f"params={json.dumps(action.params, sort_keys=True)}")
    if action.request_body is not None:
        parts.append(f"body={json.dumps(action.request_body, sort_keys=True)}")
    return " ".join(parts)


def _write_jsonl(handle, payload: dict[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=False))
    handle.write("\n")


def export(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    redis_client = get_redis_client()
    tracker = ActionTracker()
    state_manager: StateManager = tracker.state_manager
    goal_manager = GoalManager(state_manager)
    reward_calculator = RewardCalculator(goal_manager, state_manager)

    explicit_ids = _load_episode_ids(args)
    all_ids = list(explicit_ids)
    if not all_ids and (args.discover_all or not explicit_ids):
        all_ids.extend(_discover_episode_ids(redis_client, True))

    if not all_ids:
        print("[export] No episode ids provided or discovered.", file=sys.stderr)
        return 1

    if args.max_episodes is not None:
        all_ids = all_ids[: args.max_episodes]

    sft_path = output_dir / args.sft_file
    ppo_path = output_dir / args.ppo_file

    sft_handle = None
    ppo_handle = None
    try:
        if not args.skip_sft:
            sft_handle = sft_path.open("w", encoding="utf-8")
        if not args.skip_ppo:
            ppo_handle = ppo_path.open("w", encoding="utf-8")
    except OSError as exc:
        print(f"[export] Failed to open output files: {exc}", file=sys.stderr)
        return 1

    sft_written = 0
    ppo_written = 0
    try:
        for episode_id in all_ids:
            record = redis_client.get(f"episode:{episode_id}")
            if not record:
                print(f"[export] Episode {episode_id} missing in Redis, skipping.", file=sys.stderr)
                continue
            episode = json_to_model(Episode, record)
            if args.goal_id and episode.goal_id != args.goal_id:
                continue
            try:
                goal = goal_manager.get_goal(episode.goal_id)
            except ValueError:
                print(f"[export] Goal {episode.goal_id} missing for episode {episode_id}, skipping.", file=sys.stderr)
                continue

            for action_id in episode.action_history:
                try:
                    action = tracker.get_action(action_id)
                except ValueError:
                    print(f"[export] Action {action_id} missing, skipping transition.", file=sys.stderr)
                    continue

                prev_state_id = action.state_id
                next_state_id = action.next_state_id
                try:
                    prev_state = state_manager.get_state(prev_state_id, reconstruct_if_missing=True)
                    next_state = state_manager.get_state(next_state_id, reconstruct_if_missing=True)
                except Exception as exc:  # noqa: BLE001 - best-effort export
                    print(
                        f"[export] Failed to fetch states ({prev_state_id} -> {next_state_id}): {exc}.",
                        file=sys.stderr,
                    )
                    continue

                reward, done, reason = reward_calculator.compute_reward(
                    goal_id=goal.goal_id,
                    current_state_id=next_state_id,
                    previous_state_id=prev_state_id,
                    response_status=action.response_status,
                    response_body=action.response_body,
                )

                prompt = _make_prompt(goal, prev_state, prev_state_id)
                completion = _make_completion(action)

                if ppo_handle:
                    ppo_payload = {
                        "prompt": prompt,
                        "completion": completion,
                        "reward": reward,
                        "done": done,
                        "reason": reason,
                        "episode_id": episode_id,
                        "goal_id": goal.goal_id,
                        "state_id": prev_state_id,
                        "next_state_id": next_state_id,
                        "response_status": action.response_status,
                    }
                    if action.response_body is not None:
                        ppo_payload["response_body"] = action.response_body
                    _write_jsonl(ppo_handle, ppo_payload)
                    ppo_written += 1

                if sft_handle:
                    keep = done if args.done_only else (done or reward >= args.sft_min_reward)
                    if keep:
                        sft_payload = {
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": prompt},
                                {"role": "assistant", "content": completion},
                            ],
                            "metadata": {
                                "episode_id": episode_id,
                                "goal_id": goal.goal_id,
                                "state_id": prev_state_id,
                                "next_state_id": next_state_id,
                            },
                        }
                        _write_jsonl(sft_handle, sft_payload)
                        sft_written += 1

        print(
            f"[export] Done. SFT transitions: {sft_written}, PPO transitions: {ppo_written}",
            file=sys.stderr,
        )
        if sft_handle:
            print(f"[export] SFT dataset: {sft_path}")
        if ppo_handle:
            print(f"[export] PPO dataset: {ppo_path}")
        return 0
    finally:
        if sft_handle:
            sft_handle.close()
        if ppo_handle:
            ppo_handle.close()


if __name__ == "__main__":  # pragma: no cover - CLI helper
    sys.exit(export())
