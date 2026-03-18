"""Lifespan context manager factory for FastAPI applications.

Extracted from GridFlow backend/src/infrastructure/app_factory.py lines 18-26
"""

import structlog
from contextlib import asynccontextmanager
from typing import Optional, Callable, AsyncGenerator, Any, Dict
from fastapi import FastAPI

# Get a logger instance
logger = structlog.get_logger(__name__)


def create_lifespan_manager(
    on_startup: Optional[Callable] = None,
    on_shutdown: Optional[Callable] = None,
    service_name: str = "api",
    service_version: str = "1.0.0"
) -> Callable:
    """Create a lifespan factory for FastAPI application.
    
    Returns a callable compatible with FastAPI's lifespan parameter.
    
    Args:
        on_startup: Optional async function to call on startup
        on_shutdown: Optional async function to call on shutdown
        service_name: Name of the service for logging
        service_version: Version of the service for logging
    
    Returns:
        Lifespan callable for FastAPI(lifespan=...)
    
    Example:
        >>> lifespan = create_lifespan_manager(
        ...     on_startup=init_database,
        ...     service_name="my-api"
        ... )
        >>> app = FastAPI(lifespan=lifespan)
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info(
            f"{service_name} starting up",
            version=service_version,
            service=service_name,
        )
        if on_startup:
            await on_startup()
            logger.info("Startup tasks completed successfully")
        yield
        if on_shutdown:
            await on_shutdown()
            logger.info("Shutdown tasks completed successfully")
        logger.info(f"{service_name} shutting down")

    return lifespan


def create_health_check_endpoint(
    service_name: str,
    version: str = "1.0.0",
    additional_checks: Optional[Dict[str, Any]] = None
) -> Callable:
    """Create a health check endpoint function.
    
    Args:
        service_name: Name of the service
        version: Version of the service
        additional_checks: Optional dict with additional health check data
    
    Returns:
        Async function that can be used as a FastAPI endpoint
    
    Example:
        >>> app = FastAPI()
        >>> health_check = create_health_check_endpoint("my-api", "1.0.0")
        >>> app.get("/health")(health_check)
    """
    async def health_check():
        """Health check endpoint."""
        logger.info("Health check requested")
        response = {
            "status": "healthy",
            "service": service_name,
            "version": version
        }
        if additional_checks:
            response.update(additional_checks)
        return response
    
    return health_check
