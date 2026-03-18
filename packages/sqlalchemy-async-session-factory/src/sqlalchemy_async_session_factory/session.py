"""Async session factory and FastAPI dependency.

Extracted from GridFlow backend/src/database.py
"""

from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker


def create_async_session_maker(
    engine: AsyncEngine,
    expire_on_commit: bool = False,
    **kwargs
) -> async_sessionmaker[AsyncSession]:
    """Create async session maker for SQLAlchemy.
    
    Args:
        engine: AsyncEngine instance
        expire_on_commit: Expire objects on commit (default: False)
        **kwargs: Additional session maker configuration
    
    Returns:
        Configured async_sessionmaker instance
    
    Example:
        >>> from sqlalchemy.ext.asyncio import create_async_engine
        >>> engine = create_async_engine("postgresql+asyncpg://...")
        >>> SessionLocal = create_async_session_maker(engine)
        >>> 
        >>> async with SessionLocal() as session:
        ...     # Use session
        ...     pass
    """
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=expire_on_commit,
        **kwargs
    )


def create_session_dependency(
    session_maker: async_sessionmaker[AsyncSession]
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    """Create FastAPI dependency for database sessions.
    
    Returns a dependency function that provides database sessions
    to FastAPI endpoints with proper cleanup.
    
    Args:
        session_maker: async_sessionmaker instance
    
    Returns:
        Dependency function that yields AsyncSession
    
    Example:
        >>> from fastapi import FastAPI, Depends
        >>> 
        >>> SessionLocal = create_async_session_maker(engine)
        >>> get_db = create_session_dependency(SessionLocal)
        >>> 
        >>> @app.get("/items")
        >>> async def read_items(db: AsyncSession = Depends(get_db)):
        ...     # Use db session
        ...     pass
    """
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        """Provide database session to FastAPI endpoints."""
        async with session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
    
    return get_async_session
