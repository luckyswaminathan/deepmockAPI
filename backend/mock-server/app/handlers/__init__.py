from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from fastapi import Query, Request
from fastapi.responses import JSONResponse

try:
    from ..registry import SchemaRegistry
    from ..schemas import EndpointConfig, ResponseConfig
    from ..state.store import RequestState
    from ..util.timing import apply_latency
    from ..util.validation import SpecValidator
except ImportError:  # pragma: no cover
    from registry import SchemaRegistry  # type: ignore
    from schemas import EndpointConfig, ResponseConfig  # type: ignore
    from state.store import RequestState  # type: ignore
    from util.timing import apply_latency  # type: ignore
    from util.validation import SpecValidator  # type: ignore

CONTROL_QUERY_KEYS = {"latency_ms", "error_code", "seed"}


def register_handlers(
    app,
    endpoint_configs: List[EndpointConfig],
    registry: SchemaRegistry,
    validator: SpecValidator,
) -> None:
    app.state.registry = registry
    app.state.validator = validator
    app.state.endpoint_configs = endpoint_configs

    for config in endpoint_configs:
        handler = _build_handler(config, registry, validator)
        app.add_api_route(
            config.path,
            handler,
            methods=[config.method.upper()],
            name=config.operation_id,
        )


def _build_handler(
    config: EndpointConfig,
    registry: SchemaRegistry,
    validator: SpecValidator,
) -> Callable:
    async def operation(
        request: Request,
        latency_ms: Optional[int] = Query(None),
        error_code: Optional[str] = Query(None),
        seed: Optional[int] = Query(None),
    ):
        await apply_latency(latency_ms)

        request_state = await _build_request_state(request)
        params = request_state.to_dict()

        if error_code:
            response = _synthesise_error(
                config, error_code, registry, validator, params, seed
            )
            if response is not None:
                return response

        payload = registry.resolve_schema(
            config.success.schema_name, params=params, seed=seed
        )
        validator.validate(config.success.schema_name, payload)
        return JSONResponse(status_code=int(config.success.status_code), content=payload)

    return operation


async def _build_request_state(request: Request) -> RequestState:
    query_params = dict(request.query_params)
    for key in CONTROL_QUERY_KEYS:
        query_params.pop(key, None)
    body: Optional[Any] = None
    if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
        raw = await request.body()
        if raw:
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = raw.decode() if isinstance(raw, (bytes, bytearray)) else raw
    return RequestState(
        path=dict(request.path_params),
        query=query_params,
        headers=dict(request.headers),
        body=body,
    )


def _synthesise_error(
    config: EndpointConfig,
    error_code: str,
    registry: SchemaRegistry,
    validator: SpecValidator,
    params: Dict[str, Any],
    seed: Optional[int],
):
    desired = config.errors.get(error_code) or config.errors.get(str(error_code))
    if desired is None and error_code.isdigit():
        desired = config.errors.get("default")

    if desired is None:
        if error_code.isdigit():
            status = int(error_code)
        else:
            status = 500
        return JSONResponse(
            status_code=status,
            content={
                "message": f"No error schema registered for {config.operation_id}",
                "requested": error_code,
            },
        )

    payload = registry.resolve_schema(desired.schema_name, params=params, seed=seed)
    validator.validate(desired.schema_name, payload)

    status_code = desired.status_code
    if status_code == "default":
        status_code = error_code if error_code.isdigit() else "500"
    return JSONResponse(status_code=int(status_code), content=payload)
