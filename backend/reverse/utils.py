from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Optional

from ingestion import slugify


def generated_root() -> Path:
    return Path(__file__).resolve().parent / "generated"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def normalise_method(method: str) -> str:
    return method.upper()


def extract_path_params(path: str) -> list[str]:
    return [match.strip("{}") for match in re.findall(r"{([^{}]+)}", path)]


def extract_query_params(params: Iterable[dict[str, str]] | None) -> list[str]:
    if not params:
        return []
    result: list[str] = []
    for param in params:
        name = param.get("name")
        if not name:
            continue
        result.append(name)
    return result


def split_path_components(path: str) -> list[str]:
    return [segment for segment in path.strip("/").split("/") if segment and not segment.startswith("{")]


def depluralise(value: str) -> str:
    if value.endswith("ies"):
        return value[:-3] + "y"
    if value.endswith("ses"):
        return value[:-2]
    if value.endswith("s") and len(value) > 1:
        return value[:-1]
    return value


def title_case(value: str) -> str:
    parts = re.split(r"[\W_]+", value)
    return "".join(part.capitalize() for part in parts if part)


def guess_component_from_path(path: str, candidates: Iterable[str]) -> Optional[str]:
    segments = split_path_components(path)
    if not segments:
        return None
    primary = segments[-1]
    singular = depluralise(primary)
    options = {candidate.lower(): candidate for candidate in candidates}

    for key in (primary.lower(), singular.lower(), title_case(primary).lower()):
        match = options.get(key)
        if match:
            return match
    for candidate_lower, original in options.items():
        if candidate_lower.startswith(primary.lower()):
            return original
    return None
