from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI

try:  # allow running as script (no package)
    from .handlers import register_handlers
    from .registry import SchemaRegistry, load_spec
    from .schemas import collect_endpoint_configs
    from .util.validation import SpecValidator
except ImportError:  # pragma: no cover
    from handlers import register_handlers  # type: ignore
    from registry import SchemaRegistry, load_spec  # type: ignore
    from schemas import collect_endpoint_configs  # type: ignore
    from util.validation import SpecValidator  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent
SPEC_PATH = BASE_DIR / "openapi.yaml"


def create_app() -> FastAPI:
    """Instantiate the FastAPI application and register dynamic handlers."""
    spec = load_spec(SPEC_PATH)
    endpoint_configs = collect_endpoint_configs(spec)
    registry = SchemaRegistry(spec)
    validator = SpecValidator(spec)

    app = FastAPI(
        title=spec.get("info", {}).get("title", "Mock API"),
        version=spec.get("info", {}).get("version", "0.1.0"),
        description=spec.get("info", {}).get("description"),
    )

    register_handlers(app, endpoint_configs, registry, validator)
    return app


app = create_app()


def get_app_state() -> Dict[str, Any]:
    """Expose internal state for testing."""
    return {
        "registry": app.state.registry,
        "validator": app.state.validator,
        "endpoints": app.state.endpoint_configs,
    }


if __name__ == "__main__":  # convenience for local manual run
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8082, reload=True)
