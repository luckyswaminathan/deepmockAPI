from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from reverse.utils import ensure_dir, generated_root


def api_root(api_slug: str) -> Path:
    root = generated_root()
    _ensure_package(root)
    slug_root = root / api_slug
    _ensure_package(slug_root)
    return slug_root


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, default=_json_default)
        handle.write("\n")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(content)


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def list_generated_files(api_slug: str) -> list[Path]:
    root = api_root(api_slug)
    if not root.exists():
        return []
    return [path for path in root.rglob("*") if path.is_file()]


def remove_generated_folder(api_slug: str) -> None:
    root = api_root(api_slug)
    if root.exists():
        shutil.rmtree(root)


def _ensure_package(path: Path) -> None:
    ensure_dir(path)
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
