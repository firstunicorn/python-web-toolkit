"""Tests for engine factory."""

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import StaticPool
from sqlalchemy_async_session_factory import create_async_engine_with_pool


@pytest.mark.asyncio
async def test_create_async_engine_with_pool():
    """Test engine creation with SQLite (uses StaticPool)."""
    engine = create_async_engine_with_pool(
        "sqlite+aiosqlite:///:memory:",
        pool_size=5,
        echo=False,
    )

    assert isinstance(engine, AsyncEngine)
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_async_engine_custom_pool():
    """Test engine with custom pool settings (SQLite ignores pool params)."""
    engine = create_async_engine_with_pool(
        "sqlite+aiosqlite:///:memory:",
        pool_size=10,
        max_overflow=20,
        pool_timeout=60,
    )

    # SQLite uses StaticPool, pool_size params are silently ignored
    assert isinstance(engine.pool, StaticPool)
    await engine.dispose()
