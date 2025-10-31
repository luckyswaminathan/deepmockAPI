"""API package containing routers and schemas for the DeepMock backend."""

from .routes.apis import router as apis_router  # noqa: F401
from .routes.reverse import router as reverse_router  # noqa: F401
from .routes.views import router as views_router  # noqa: F401

__all__ = ["apis_router", "reverse_router", "views_router"]
