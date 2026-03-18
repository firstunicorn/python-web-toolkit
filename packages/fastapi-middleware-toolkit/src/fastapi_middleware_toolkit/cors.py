"""CORS middleware setup for FastAPI applications.

Extracted from GridFlow backend/src/infrastructure/app_factory.py lines 46-59
"""

from typing import List, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors_middleware(
    app: FastAPI,
    allowed_origins: Union[str, List[str]],
    allow_credentials: bool = False,
    allowed_methods: List[str] = None,
    allowed_headers: List[str] = None,
    max_age: int = 600
) -> None:
    """Setup CORS middleware with secure defaults.
    
    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed origins or single origin string
        allow_credentials: Whether to allow credentials (cookies, auth headers)
        allowed_methods: HTTP methods to allow (default: ["GET", "POST"])
        allowed_headers: Headers to allow (default: standard headers)
        max_age: Preflight cache time in seconds (default: 600)
    
    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> setup_cors_middleware(
        ...     app,
        ...     allowed_origins=["http://localhost:3000"],
        ...     allow_credentials=False
        ... )
    """
    # Default to secure methods if not specified
    if allowed_methods is None:
        allowed_methods = ["GET", "POST"]
    
    # Default to standard headers if not specified
    if allowed_headers is None:
        allowed_headers = [
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "X-Requested-With"
        ]
    
    # Handle single string origin
    if isinstance(allowed_origins, str):
        if allowed_origins.strip() == "*":
            origins_list = ["*"]
        else:
            origins_list = [i.strip() for i in allowed_origins.split(",")]
    else:
        origins_list = allowed_origins
    
    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_list,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
        max_age=max_age,
    )
