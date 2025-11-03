"""Standalone FastAPI application for Stripe API mock."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from code.routes import router

app = FastAPI(
    title="Stripe API Mock",
    description="Generated mock API for Stripe",
    version="1.0.0",
)

# CORS: allow all origins for a standalone mock API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the generated routes
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "stripe-api-mock"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

