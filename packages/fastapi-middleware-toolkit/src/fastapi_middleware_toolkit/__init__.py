"""FastAPI Middleware Toolkit - Reusable middleware setup functions."""

from fastapi_middleware_toolkit.cors import setup_cors_middleware
from fastapi_middleware_toolkit.error_handlers import setup_error_handlers
from fastapi_middleware_toolkit.lifespan import (
    create_lifespan_manager,
    create_health_check_endpoint
)
from fastapi_middleware_toolkit.cache_control import (
    setup_cache_control_middleware,
    CacheControlMiddleware
)

__version__ = "0.1.0"

__all__ = [
    "setup_cors_middleware",
    "setup_error_handlers",
    "create_lifespan_manager",
    "create_health_check_endpoint",
    "setup_cache_control_middleware",
    "CacheControlMiddleware",
]
