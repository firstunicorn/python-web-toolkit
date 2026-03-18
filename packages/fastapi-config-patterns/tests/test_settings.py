"""Tests for settings classes."""

import pytest
from fastapi_config_patterns import (
    BaseFastAPISettings,
    BaseDatabaseSettings,
    assemble_cors_origins,
)


def test_base_fastapi_settings_defaults():
    """Test BaseFastAPISettings accepts explicit values."""
    settings = BaseFastAPISettings(
        debug=False,
        host="0.0.0.0",
        port=8000,
        allowed_origins=["http://localhost:3000"],
        cors_allow_credentials=False,
        cors_max_age=600,
    )

    assert settings.debug is False
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.api_v1_str == "/v1"
    assert settings.cors_allow_credentials is False
    assert settings.cors_max_age == 600


def test_base_database_settings():
    """Test BaseDatabaseSettings."""
    settings = BaseDatabaseSettings(
        database_url="postgresql+asyncpg://user:pass@localhost/db"
    )

    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_combined_settings():
    """Test combining multiple settings classes."""

    class AppSettings(BaseFastAPISettings, BaseDatabaseSettings):
        app_name: str = "test-app"

    settings = AppSettings(
        debug=False,
        database_url="postgresql+asyncpg://user:pass@localhost/db",
    )

    assert settings.debug is False
    assert settings.database_url is not None
    assert settings.app_name == "test-app"


def test_assemble_cors_origins_from_string():
    """Test CORS origins parsing from comma-separated string."""
    result = assemble_cors_origins(
        "http://localhost:3000,http://localhost:8080"
    )
    assert result == ["http://localhost:3000", "http://localhost:8080"]


def test_assemble_cors_origins_wildcard():
    """Test CORS origins with wildcard."""
    result = assemble_cors_origins("*")
    assert result == ["*"]


def test_assemble_cors_origins_from_list():
    """Test CORS origins parsing from list."""
    result = assemble_cors_origins(
        ["http://localhost:3000", "http://localhost:8080"]
    )
    assert result == ["http://localhost:3000", "http://localhost:8080"]
