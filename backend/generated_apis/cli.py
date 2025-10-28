from __future__ import annotations

import argparse
import sys
from pathlib import Path


def run_tests() -> None:
    parser = argparse.ArgumentParser(description="Run pytest against a generated API package.")
    parser.add_argument(
        "--api-slug",
        required=True,
        help="Slug of the generated API to test.",
    )
    args, remaining = parser.parse_known_args()

    package_dir = Path(__file__).resolve().parent / args.api_slug
    tests_dir = package_dir / "tests"

    if not package_dir.exists():
        print(f"Generated API package '{args.api_slug}' not found.", file=sys.stderr)
        sys.exit(2)

    if not tests_dir.exists():
        print(f"No tests directory found for '{args.api_slug}'.", file=sys.stderr)
        sys.exit(3)

    try:
        import pytest  # type: ignore
    except ImportError:  # pragma: no cover - guard for runtime usage
        print("pytest is required to run generated tests. Install it and retry.", file=sys.stderr)
        sys.exit(4)

    exit_code = pytest.main([str(tests_dir), *remaining])
    sys.exit(exit_code)


def main() -> None:
    run_tests()


if __name__ == "__main__":  # pragma: no cover
    main()
