"""Base FastAPI settings patterns.

Extracted from GridFlow backend/src/config.py
"""

from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BaseFastAPISettings(BaseSettings):
    """Base settings for FastAPI applications.
    
    Provides common configuration fields that most FastAPI apps need.
    Extend this class in your project to add app-specific settings.
    
    Example:
        >>> class MyAppSettings(BaseFastAPISettings):
        ...     app_name: str = "my-app"
        ...     
        >>> settings = MyAppSettings()
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    debug: bool = False
    api_v1_str: str = "/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    allowed_origins: Union[str, List[str]] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
    )
    cors_allow_credentials: bool = False
    cors_max_age: int = 600  # 10 minutes preflight cache
