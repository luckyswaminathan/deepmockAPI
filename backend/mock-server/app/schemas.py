from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

REF_RE = re.compile(r"^#/components/schemas/(?P<name>[^/]+)$")

HTTP_METHODS = {"get", "put", "post", "delete", "patch", "options", "head"}


@dataclass(frozen=True)
class ResponseConfig:
    status_code: str
    media_type: str
    schema_name: str


@dataclass(frozen=True)
class EndpointConfig:
    path: str
    method: str
    operation_id: str
    success: ResponseConfig
    errors: Dict[str, ResponseConfig]


def _ensure_components(spec: Dict[str, Any]) -> Dict[str, Any]:
    components = spec.setdefault("components", {})
    schemas = components.setdefault("schemas", {})
    return schemas


def _sanitize_name(name: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_")
    if not cleaned:
        return "InlineSchema"
    if cleaned[0].isdigit():
        cleaned = f"Schema_{cleaned}"
    return cleaned


def ensure_named_schema(
    spec: Dict[str, Any], schema_obj: Dict[str, Any], name_hint: str
) -> str:
    """Return the schema name, adding inline schemas to components as needed."""
    if "$ref" in schema_obj:
        match = REF_RE.match(schema_obj["$ref"])
        if match:
            return match.group("name")
        raise ValueError(f"Unsupported external $ref: {schema_obj['$ref']}")

    schemas = _ensure_components(spec)
    base_name = _sanitize_name(name_hint)
    candidate = base_name
    counter = 1
    while candidate in schemas:
        counter += 1
        candidate = f"{base_name}_{counter}"

    schemas[candidate] = copy.deepcopy(schema_obj)
    return candidate


def _select_response_schema(
    responses: Dict[str, Any], name_hint: str
) -> Optional[Tuple[str, Dict[str, Any], str]]:
    """Pick preferred response schema: prefer application/json among 2xx."""
    def iter_candidates() -> Iterable[Tuple[str, Dict[str, Any]]]:
        for status, payload in responses.items():
            if not status:
                continue
            if status.lower() == "default":
                continue
            try:
                code = int(status)
            except ValueError:
                continue
            if 200 <= code <= 299:
                yield status, payload

    for status, payload in sorted(iter_candidates(), key=lambda item: int(item[0])):  # type: ignore[arg-type]
        content = payload.get("content") or {}
        if not content:
            continue
        if "application/json" in content:
            return status, content["application/json"], "application/json"
        media_type, body = next(iter(content.items()))
        return status, body, media_type
    return None


def _collect_error_responses(
    spec: Dict[str, Any], responses: Dict[str, Any], name_hint: str
) -> Dict[str, ResponseConfig]:
    errors: Dict[str, ResponseConfig] = {}
    for status, payload in responses.items():
        if status.lower() == "default":
            status_key = "default"
        else:
            status_key = status
        if status_key in errors:
            continue
        if status.lower() == "default":
            schema_hint = f"{name_hint}_default"
        else:
            try:
                code = int(status)
            except ValueError:
                continue
            if 200 <= code <= 299:
                continue
            schema_hint = f"{name_hint}_{status}"
        content = payload.get("content") or {}
        if not content:
            continue
        if "application/json" in content:
            media_type = "application/json"
            schema_obj = content["application/json"].get("schema")
        else:
            media_type, media_payload = next(iter(content.items()))
            schema_obj = media_payload.get("schema")
        if not schema_obj:
            continue
        schema_name = ensure_named_schema(spec, schema_obj, schema_hint)
        errors[status_key] = ResponseConfig(
            status_code=status_key,
            media_type=media_type,
            schema_name=schema_name,
        )
    return errors


def collect_endpoint_configs(spec: Dict[str, Any]) -> List[EndpointConfig]:
    """Gather endpoint metadata and ensure schemas are named."""
    endpoints: List[EndpointConfig] = []
    paths = spec.get("paths", {}) or {}

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                continue
            responses = operation.get("responses") or {}
            choice = _select_response_schema(responses, f"{method}_{path}")
            if not choice:
                continue
            status_code, media_payload, media_type = choice
            schema_obj = media_payload.get("schema")
            if not schema_obj:
                continue
            operation_id = operation.get("operationId") or _sanitize_name(
                f"{method}_{path}"
            )
            schema_name = ensure_named_schema(
                spec, schema_obj, f"{operation_id}_{status_code}"
            )
            error_configs = _collect_error_responses(
                spec, responses, f"{operation_id}_error"
            )
            endpoints.append(
                EndpointConfig(
                    path=path,
                    method=method.lower(),
                    operation_id=operation_id,
                    success=ResponseConfig(
                        status_code=status_code,
                        media_type=media_type,
                        schema_name=schema_name,
                    ),
                    errors=error_configs,
                )
            )
    return endpoints
