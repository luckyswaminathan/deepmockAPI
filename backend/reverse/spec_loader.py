from __future__ import annotations

import json
from typing import Any, Dict, Optional

from ingestion import parse_openapi_spec, slugify
from reverse.models import ReverseIngestionResult, RouteInventoryEntry
from reverse.storage import api_root, write_json
from reverse.utils import (
    ensure_dir,
    extract_path_params,
    extract_query_params,
    normalise_method,
)


HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


def _load_request_body_ref(operation: Dict[str, Any]) -> Optional[str]:
    request_body = operation.get("requestBody")
    if not isinstance(request_body, dict):
        return None
    content = request_body.get("content")
    if not isinstance(content, dict):
        return None
    for media in ("application/json", "application/*+json"):
        definition = content.get(media)
        if isinstance(definition, dict):
            schema = definition.get("schema")
            if isinstance(schema, dict):
                ref = schema.get("$ref")
                if isinstance(ref, str):
                    return ref
    for definition in content.values():
        if isinstance(definition, dict):
            schema = definition.get("schema")
            if isinstance(schema, dict):
                ref = schema.get("$ref")
                if isinstance(ref, str):
                    return ref
    return None


def _load_response_ref(operation: Dict[str, Any]) -> Optional[str]:
    responses = operation.get("responses")
    if not isinstance(responses, dict):
        return None
    preferred_statuses = ["200", "201", "202", "default"]
    status_keys = list(responses.keys())
    for status in preferred_statuses + status_keys:
        entry = responses.get(status)
        if not isinstance(entry, dict):
            continue
        content = entry.get("content")
        if not isinstance(content, dict):
            continue
        for definition in content.values():
            if isinstance(definition, dict):
                schema = definition.get("schema")
                if isinstance(schema, dict):
                    ref = schema.get("$ref")
                    if isinstance(ref, str):
                        return ref
    return None


def ingest_spec(raw_spec: str | Dict[str, Any], *, explicit_name: Optional[str] = None) -> ReverseIngestionResult:
    if isinstance(raw_spec, str):
        payload = parse_openapi_spec(raw_spec)
    elif isinstance(raw_spec, dict):
        payload = raw_spec
    else:
        raise TypeError("raw_spec must be a JSON string or a dictionary.")

    info = payload.get("info", {}) if isinstance(payload, dict) else {}
    api_name = explicit_name or info.get("title") or "API"
    api_slug = slugify(api_name)
    version = info.get("version")

    paths = payload.get("paths", {}) if isinstance(payload, dict) else {}
    route_inventory: list[RouteInventoryEntry] = []
    for path, definition in paths.items():
        if not isinstance(definition, dict):
            continue
        shared_params = definition.get("parameters")
        for method, operation in definition.items():
            if method not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                continue
            method_upper = normalise_method(method)
            parameters: list[dict[str, Any]] = []
            if isinstance(shared_params, list):
                parameters.extend(item for item in shared_params if isinstance(item, dict))
            op_params = operation.get("parameters")
            if isinstance(op_params, list):
                parameters.extend(item for item in op_params if isinstance(item, dict))
            path_params = [param["name"] for param in parameters if param.get("in") == "path" and isinstance(param.get("name"), str)]
            if not path_params:
                path_params = extract_path_params(path)
            query_params = [param["name"] for param in parameters if param.get("in") == "query" and isinstance(param.get("name"), str)]

            entry = RouteInventoryEntry(
                method=method_upper,
                path=path,
                operation_id=operation.get("operationId"),
                summary=operation.get("summary"),
                tags=[tag for tag in operation.get("tags", []) if isinstance(tag, str)],
                request_body_ref=_load_request_body_ref(operation),
                response_body_ref=_load_response_ref(operation),
                path_parameters=path_params,
                query_parameters=query_params or extract_query_params(parameters),
            )
            route_inventory.append(entry)

    root = api_root(api_slug)
    ensure_dir(root)
    write_json(root / "source" / "openapi.json", payload)
    inventory_payload = [entry.dict() for entry in route_inventory]
    write_json(root / "plan" / "route_inventory.json", inventory_payload)

    return ReverseIngestionResult(
        api_slug=api_slug,
        api_name=api_name,
        version=version,
        route_inventory=route_inventory,
    )
