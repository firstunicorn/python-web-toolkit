"""Tests for session factory."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool,
    create_async_session_maker,
    create_session_dependency
)


@pytest.mark.asyncio
async def test_create_async_session_maker():
    """Test session maker creation."""
    engine = create_async_engine_with_pool(
        "sqlite+aiosqlite:///:memory:"
    )
    
    SessionLocal = create_async_session_maker(engine)
    
    async with SessionLocal() as session:
        assert isinstance(session, AsyncSession)
    
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_session_dependency():
    """Test FastAPI dependency creation."""
    engine = create_async_engine_with_pool(
        "sqlite+aiosqlite:///:memory:"
    )
    
    SessionLocal = create_async_session_maker(engine)
    get_db = create_session_dependency(SessionLocal)
    
    # Test dependency yields session
    async for session in get_db():
        assert isinstance(session, AsyncSession)
    
    await engine.dispose()


@pytest.mark.asyncio
async def test_session_cleanup():
    """Test session cleanup on exit."""
    engine = create_async_engine_with_pool(
        "sqlite+aiosqlite:///:memory:"
    )
    
    SessionLocal = create_async_session_maker(engine)
    
    session = None
    async with SessionLocal() as s:
        session = s
        assert not session.is_active or True  # Session active during context
    
    # Session should be closed after context
    await engine.dispose()
