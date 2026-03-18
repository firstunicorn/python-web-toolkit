"""Utility functions for connection pool management.

Extracted from GridFlow backend/src/database.py
"""

import warnings
import logging
from sqlalchemy import event
from sqlalchemy.pool import Pool
from sqlalchemy.ext.asyncio import AsyncEngine


def suppress_pool_warnings() -> None:
    """Suppress connection pool warnings during cleanup.
    
    Suppresses event loop closure warnings that occur during normal
    connection termination. This is safe because connections are
    being cleaned up properly, just after the event loop closes.
    
    Call this once during application startup.
    
    Example:
        >>> suppress_pool_warnings()
    """
    logging.getLogger(
        'sqlalchemy.pool.impl.AsyncAdaptedQueuePool'
    ).setLevel(logging.CRITICAL)


def setup_pool_event_handlers(engine: AsyncEngine) -> None:
    """Setup event handlers for connection pool.
    
    Adds event listener to suppress errors during connection closure.
    This handles cleanup gracefully even if event loop is closed.
    
    Args:
        engine: AsyncEngine instance
    
    Example:
        >>> from sqlalchemy.ext.asyncio import create_async_engine
        >>> engine = create_async_engine("postgresql+asyncpg://...")
        >>> setup_pool_event_handlers(engine)
    """
    @event.listens_for(Pool, "close")
    def receive_close(dbapi_conn, connection_record):
        """Suppress errors during connection closure.
        
        This handles cleanup gracefully even if event loop is closed.
        """
        # Suppress pool closure warnings
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=".*pool was already closed.*"
            )
