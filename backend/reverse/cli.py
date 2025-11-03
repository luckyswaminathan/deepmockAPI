from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from database import init_core_tables
from reverse.generator import generate
from reverse.models import GenerationReport, ReversePlan
from reverse.storage import read_json


def _load_plan(path: Path) -> ReversePlan:
    payload = read_json(path)
    try:
        return ReversePlan.parse_obj(payload)
    except Exception as exc:  # pragma: no cover - defensive logging for CLI usage
        raise RuntimeError(f"Unable to parse plan file at '{path}': {exc}") from exc


def _emit_report(report: GenerationReport, *, output_path: Optional[Path]) -> None:
    payload = report.dict()
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        sys.stdout.flush()


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate scaffolding for a previously ingested API slug."
    )
    parser.add_argument(
        "--api-slug",
        required=True,
        help="API identifier that matches the slug used during ingestion.",
    )
    parser.add_argument(
        "--plan-json",
        type=Path,
        help="Optional explicit plan JSON file to hydrate instead of rebuilding from route inventory.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        help="Optional path to write the generation report as JSON. Defaults to stdout.",
    )

    args = parser.parse_args(argv)

    # Initialize database tables before generation
    try:
        init_core_tables()
    except RuntimeError as exc:
        raise RuntimeError(
            f"Failed to initialize database: {exc}. "
            "Ensure _DATABASE_URL environment variable is set correctly."
        ) from exc

    plan: ReversePlan | None = None
    if args.plan_json:
        plan = _load_plan(args.plan_json)

    report = generate(plan, args.api_slug)
    _emit_report(report, output_path=args.report_json)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
