from __future__ import annotations

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


@app.on_event("startup")
def on_startup() -> None:
    try:
        init_core_tables()
    except RuntimeError as exc:
        raise RuntimeError(
            "Failed to initialize database connection. "
            "Ensure DATABASE_URL is set to a valid PostgreSQL connection string."
        ) from exc


app.include_router(apis_router)
app.include_router(reverse_router)
app.include_router(views_router)


if __name__ == "__main__":
    # Enable local development with: python backend/main.py
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
