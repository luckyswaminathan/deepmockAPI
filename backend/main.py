from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:  # When loaded as backend.main
    from .api import apis_router, reverse_router, views_router
    from .database import init_core_tables
except ImportError:  # pragma: no cover - allow running as a standalone script
    from api import apis_router, reverse_router, views_router  # type: ignore
    from database import init_core_tables  # type: ignore

app = FastAPI(title="DeepMock API Backend")

# CORS: allow local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RL Middleware (if enabled)
if os.getenv("RL_ENABLED", "false").lower() == "true":
    try:
        from rl.middleware import RLMiddleware
        from rl.redis_client import ensure_lfu_policy
        
        app.add_middleware(RLMiddleware, enabled=True)
        print("[main] RL middleware enabled")
    except ImportError as e:
        print(f"[main] Warning: Could not import RL middleware: {e}")


@app.on_event("startup")
def on_startup() -> None:
    try:
        init_core_tables()
    except Exception as exc:
        # More detailed error handling
        import sys
        print(f"[main] ERROR: Failed to initialize database: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise RuntimeError(
            "Failed to initialize database connection. "
            "Ensure _DATABASE_URL is set to a valid PostgreSQL connection string. "
            f"Error: {exc}"
        ) from exc
    
    # Initialize Redis LFU policy if RL enabled
    if os.getenv("RL_ENABLED", "false").lower() == "true":
        try:
            from rl.redis_client import ensure_lfu_policy
            ensure_lfu_policy()
        except Exception as e:
            print(f"[main] Warning: Could not configure Redis LFU policy: {e}")
    
    # Auto-mount all generated APIs
    try:
        from reverse import runtime
        generated_apis = runtime.discover_generated_apis()
        for api_slug in generated_apis:
            try:
                runtime.mount_generated_routes(app, api_slug, prefix=f"/generated/{api_slug}")
                print(f"[main] Auto-mounted generated API: {api_slug}")
            except Exception as e:
                print(f"[main] Warning: Could not mount API '{api_slug}': {e}")
    except Exception as e:
        print(f"[main] Warning: Could not discover generated APIs: {e}")


app.include_router(apis_router)
app.include_router(reverse_router)
app.include_router(views_router)

# RL Routes (if enabled)
if os.getenv("RL_ENABLED", "false").lower() == "true":
    try:
        from api.routes import rl
        app.include_router(rl.router)
        print("[main] RL routes enabled")
    except ImportError as e:
        print(f"[main] Warning: Could not import RL routes: {e}")


if __name__ == "__main__":
    # Enable local development with: python backend/main.py
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
