"""FastAPI Config Patterns - Reusable Pydantic settings classes."""

from fastapi_config_patterns.base_settings import BaseFastAPISettings
from fastapi_config_patterns.database_settings import BaseDatabaseSettings
from fastapi_config_patterns.validators import assemble_cors_origins

__version__ = "0.1.0"

__all__ = [
    "BaseFastAPISettings",
    "BaseDatabaseSettings",
    "assemble_cors_origins",
]
