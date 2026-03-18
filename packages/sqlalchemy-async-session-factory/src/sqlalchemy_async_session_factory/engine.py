"""Async engine factory with connection pooling.

Extracted from GridFlow backend/src/database.py
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import StaticPool


def _is_sqlite(database_url: str) -> bool:
    """Check if the database URL targets SQLite."""
    return "sqlite" in database_url.lower()


def create_async_engine_with_pool(
    database_url: str,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 5,
    pool_timeout: int = 30,
    pool_pre_ping: bool = True,
    pool_recycle: int = 300,
    **kwargs,
) -> AsyncEngine:
    """Create async SQLAlchemy engine with connection pooling.

    Optimized for PostgreSQL with asyncpg driver. Also supports SQLite
    with aiosqlite driver (uses StaticPool, ignores pool params).

    Args:
        database_url: Database connection URL
        echo: Echo SQL queries (default: False)
        pool_size: Connections in pool (ignored for SQLite)
        max_overflow: Max overflow connections (ignored for SQLite)
        pool_timeout: Connection timeout seconds (ignored for SQLite)
        pool_pre_ping: Test connections before use (default: True)
        pool_recycle: Recycle connections after seconds (default: 300)
        **kwargs: Additional engine configuration

    Returns:
        Configured AsyncEngine instance

    Example:
        >>> engine = create_async_engine_with_pool(
        ...     "postgresql+asyncpg://user:pass@localhost/db",
        ...     pool_size=10,
        ... )
    """
    engine_kwargs = {"echo": echo, "future": True, **kwargs}

    if _is_sqlite(database_url):
        engine_kwargs.setdefault("poolclass", StaticPool)
        engine_kwargs.setdefault(
            "connect_args", {"check_same_thread": False}
        )
    else:
        engine_kwargs.update(
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_pre_ping=pool_pre_ping,
            pool_recycle=pool_recycle,
        )

    return create_async_engine(database_url, **engine_kwargs)
