"""Global error handling middleware for FastAPI applications.

Extracted from GridFlow backend/src/middleware/error_handler.py
"""

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from typing import Optional, Type

# Get a logger instance
logger = structlog.get_logger(__name__)


def setup_error_handlers(
    app: FastAPI,
    custom_exception_class: Optional[Type[Exception]] = None
) -> None:
    """Setup global error handlers for the FastAPI application.
    
    Args:
        app: FastAPI application instance
        custom_exception_class: Optional custom exception class to handle
    
    Example:
        >>> from fastapi import FastAPI
        >>> from python_app_exceptions import BaseApplicationException
        >>> app = FastAPI()
        >>> setup_error_handlers(app, BaseApplicationException)
    """

    # Handle custom application exceptions if class provided
    if custom_exception_class:
        @app.exception_handler(custom_exception_class)
        async def custom_exception_handler(
            request: Request, 
            exc: custom_exception_class
        ):
            """Handle custom application exceptions."""
            logger.warning(
                "Application exception occurred",
                exception_type=type(exc).__name__,
                message=getattr(exc, 'message', str(exc)),
                details=getattr(exc, 'details', None),
                path=str(request.url),
                method=request.method
            )
            return JSONResponse(
                status_code=400,
                content={
                    "detail": getattr(exc, 'message', str(exc)),
                    "error_type": type(exc).__name__,
                    "details": getattr(exc, 'details', None)
                }
            )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.info(
            "HTTP exception occurred",
            status_code=exc.status_code,
            detail=exc.detail,
            path=str(request.url),
            method=request.method
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        """Handle request validation errors."""
        logger.warning(
            "Validation error occurred",
            errors=exc.errors(),
            path=str(request.url),
            method=request.method
        )
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        logger.error(
            "Unhandled exception occurred",
            exception_type=type(exc).__name__,
            exception_message=str(exc),
            path=str(request.url),
            method=request.method,
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_type": type(exc).__name__
            }
        )
