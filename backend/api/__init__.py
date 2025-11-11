"""API package containing routers and schemas for the DeepMock backend."""

import os

from .routes.apis import router as apis_router  # noqa: F401
from .routes.reverse import router as reverse_router  # noqa: F401
from .routes.views import router as views_router  # noqa: F401

# Conditionally import RL router
if os.getenv("RL_ENABLED", "false").lower() == "true":
    from .routes.rl import router as rl_router  # noqa: F401
    __all__ = ["apis_router", "reverse_router", "views_router", "rl_router"]
else:
    __all__ = ["apis_router", "reverse_router", "views_router"]
