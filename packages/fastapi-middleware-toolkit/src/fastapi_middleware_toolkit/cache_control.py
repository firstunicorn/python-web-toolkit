"""Cache-Control middleware for FastAPI applications.

Sets safe default Cache-Control headers if route didn't set them.
"""
import structlog
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Optional

logger = structlog.get_logger(__name__)


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Middleware that sets default Cache-Control headers if not set by route.
    
    Prevents accidental caching of sensitive data by setting safe defaults.
    Routes can override by setting Cache-Control explicitly.
    
    Args:
        default_cache_control: Default header value to use.
            Default: "public, max-age=60, stale-while-revalidate=30"
    
    Examples:
        >>> app = FastAPI()
        >>> app.add_middleware(
        ...     CacheControlMiddleware,
        ...     default_cache_control="no-store"
        ... )
    """
    
    def __init__(
        self,
        app,
        default_cache_control: str = "public, max-age=60, stale-while-revalidate=30"
    ):
        super().__init__(app)
        self.default_cache_control = default_cache_control
        logger.info(
            "cache_control_middleware_initialized",
            default_policy=default_cache_control
        )
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Process request and set Cache-Control if not already set."""
        response = await call_next(request)
        
        if "cache-control" not in response.headers:
            response.headers["Cache-Control"] = self.default_cache_control
            logger.debug(
                "cache_control_header_set",
                path=request.url.path,
                policy=self.default_cache_control
            )
        
        return response


def setup_cache_control_middleware(
    app: FastAPI,
    default_cache_control: str = "public, max-age=60, stale-while-revalidate=30"
) -> None:
    """Setup Cache-Control middleware for FastAPI application.
    
    Sets safe default Cache-Control headers if routes don't set them.
    
    Args:
        app: FastAPI application instance
        default_cache_control: Default header value to use.
            Default: "public, max-age=60, stale-while-revalidate=30"
    
    Common patterns:
        - "public, max-age=60, stale-while-revalidate=30" (default, moderate caching)
        - "no-store" (no caching, for sensitive data)
        - "public, max-age=3600" (1 hour cache)
        - "private, max-age=0, must-revalidate" (browser only, always validate)
    
    Examples:
        >>> app = FastAPI()
        >>> setup_cache_control_middleware(app)
        >>> setup_cache_control_middleware(app, "no-store")
    """
    app.add_middleware(CacheControlMiddleware, default_cache_control=default_cache_control)
    logger.info("cache_control_middleware_setup", default_policy=default_cache_control)
