"""Utility to upload datasets and kick off OpenAI fine-tuning/RL jobs."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload dataset files and trigger OpenAI fine-tune / RL jobs.",
    )
    parser.add_argument("--api-base", default="https://api.openai.com", help="OpenAI API base URL.")
    parser.add_argument("--api-key", help="API key (defaults to OPENAI_API_KEY env var).")
    parser.add_argument("--sft-file", type=Path, help="Path to the SFT JSONL file to upload.")
    parser.add_argument("--sft-model", default="gpt-4.1-mini", help="Base model for SFT fine-tuning.")
    parser.add_argument("--sft-suffix", help="Optional suffix for the resulting SFT model name.")
    parser.add_argument("--ppo-file", type=Path, help="Path to the PPO/RL JSONL dataset.")
    parser.add_argument("--ppo-model", help="Model (usually the SFT result) to continue RL fine-tuning.")
    parser.add_argument("--ppo-algorithm", default="ppo", help="RL algorithm name to send to the API.")
    parser.add_argument("--purpose-sft", default="fine-tune", help="Purpose used when uploading the SFT file.")
    parser.add_argument("--purpose-ppo", default="rl", help="Purpose used when uploading the PPO dataset.")
    parser.add_argument("--dry-run", action="store_true", help="Print the steps without calling the API.")
    return parser.parse_args(argv)


def _require_key(args: argparse.Namespace) -> str:
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY environment variable (or --api-key) is required")
    return api_key


def _upload_file(
    path: Path,
    purpose: str,
    api_base: str,
    api_key: str,
    dry_run: bool = False,
) -> Optional[str]:
    if path is None:
        return None
    if not path.exists():
        raise SystemExit(f"Dataset file not found: {path}")
    
    # Validate file is not empty and has valid JSONL content
    try:
        with path.open("r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]
            if not lines:
                raise SystemExit(
                    f"Dataset file {path} is empty. "
                    f"For SFT files, ensure examples meet the reward threshold (try --sft-min-reward 0 or lower)."
                )
            # Validate first line is valid JSON
            try:
                json.loads(lines[0])
            except json.JSONDecodeError as e:
                raise SystemExit(f"Dataset file {path} contains invalid JSON on first line: {e}")
    except UnicodeDecodeError:
        # If it's not text, assume it's binary and skip validation
        pass
    
    if dry_run:
        print(f"[finetune] DRY-RUN upload {path} ({purpose})")
        return f"dryrun-{path.stem}"
    with path.open("rb") as handle:
        resp = requests.post(
            f"{api_base}/v1/files",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (path.name, handle)},
            data={"purpose": purpose},
            timeout=300,
        )
    if resp.status_code >= 400:
        raise SystemExit(f"Failed to upload {path}: {resp.status_code} {resp.text}")
    data = resp.json()
    file_id = data.get("id")
    print(f"[finetune] Uploaded {path.name} -> {file_id}")
    return file_id


def _create_sft_job(
    training_file: str,
    model: str,
    suffix: Optional[str],
    api_base: str,
    api_key: str,
    dry_run: bool,
) -> Optional[str]:
    if dry_run:
        print(f"[finetune] DRY-RUN create SFT job model={model} file={training_file} suffix={suffix}")
        return "ft-dryrun"
    payload = {"training_file": training_file, "model": model}
    if suffix:
        payload["suffix"] = suffix
    resp = requests.post(
        f"{api_base}/v1/fine_tuning/jobs",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    if resp.status_code >= 400:
        raise SystemExit(f"Failed to start SFT job: {resp.status_code} {resp.text}")
    data = resp.json()
    job_id = data.get("id")
    result_model = data.get("fine_tuned_model")
    print(f"[finetune] SFT job {job_id} started (model -> {result_model or 'pending'})")
    return result_model


def _create_rl_job(
    dataset_id: str,
    model: str,
    algorithm: str,
    api_base: str,
    api_key: str,
    dry_run: bool,
) -> Optional[str]:
    if dry_run:
        print(
            f"[finetune] DRY-RUN create RL job model={model} dataset={dataset_id} algorithm={algorithm}"
        )
        return "rl-dryrun"
    payload = {"model": model, "dataset_id": dataset_id, "algorithm": algorithm}
    resp = requests.post(
        f"{api_base}/v1/rl/fine_tuning/jobs",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    if resp.status_code >= 400:
        raise SystemExit(f"Failed to start RL job: {resp.status_code} {resp.text}")
    data = resp.json()
    job_id = data.get("id")
    print(f"[finetune] RL job {job_id} started against model {model}")
    return job_id


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    api_key = _require_key(args)

    if not args.sft_file and not args.ppo_file:
        raise SystemExit("Provide --sft-file, --ppo-file, or both.")

    sft_file_id = None
    if args.sft_file:
        sft_file_id = _upload_file(
            args.sft_file,
            args.purpose_sft,
            args.api_base,
            api_key,
            args.dry_run,
        )

    sft_result_model = None
    if args.sft_file and sft_file_id:
        sft_result_model = _create_sft_job(
            training_file=sft_file_id,
            model=args.sft_model,
            suffix=args.sft_suffix,
            api_base=args.api_base,
            api_key=api_key,
            dry_run=args.dry_run,
        )

    ppo_file_id = None
    if args.ppo_file:
        target_model = args.ppo_model or sft_result_model
        if not target_model:
            raise SystemExit("--ppo-model is required when no SFT job is requested or still pending.")
        ppo_file_id = _upload_file(
            args.ppo_file,
            args.purpose_ppo,
            args.api_base,
            api_key,
            args.dry_run,
        )
        if ppo_file_id:
            _create_rl_job(
                dataset_id=ppo_file_id,
                model=target_model,
                algorithm=args.ppo_algorithm,
                api_base=args.api_base,
                api_key=api_key,
                dry_run=args.dry_run,
            )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI helper
    sys.exit(main())
