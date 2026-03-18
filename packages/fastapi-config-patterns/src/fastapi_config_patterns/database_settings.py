"""Database settings mixin.

Extracted from GridFlow backend/src/config.py
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BaseDatabaseSettings(BaseSettings):
    """Database settings mixin for FastAPI applications.
    
    Provides database connection configuration. Use as a mixin with
    BaseFastAPISettings or other settings classes.
    
    Supports both PostgreSQL and SQLite with async drivers.
    
    Example:
        >>> class MyAppSettings(BaseFastAPISettings, BaseDatabaseSettings):
        ...     pass
        >>> 
        >>> settings = MyAppSettings()
        >>> print(settings.database_url)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # PostgreSQL default (recommended for production)
    database_url: str = Field(
        default="postgresql+asyncpg://user:pass@localhost:5432/db",
    )
