# SQLAlchemy Async Session Factory

Factory functions for SQLAlchemy async engine and session management with FastAPI integration.

**Extracted from:** GridFlow `backend/src/database.py`

## Installation

```bash
# PostgreSQL support (recommended)
pip install sqlalchemy-async-session-factory

# SQLite support
pip install sqlalchemy-async-session-factory[sqlite]
```

## Features

- **Engine Factory**: Create async engine with connection pooling
- **Session Factory**: Create async session maker
- **FastAPI Dependency**: Generate session dependency for FastAPI
- **Pool Management**: Connection pool event handlers and warning suppression

## Usage

### Basic Setup

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool,
    create_async_session_maker,
    create_session_dependency,
    suppress_pool_warnings
)

# Suppress pool warnings (call once at startup)
suppress_pool_warnings()

# Create engine
engine = create_async_engine_with_pool(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=10,
    echo=True
)

# Create session maker
SessionLocal = create_async_session_maker(engine)

# Create FastAPI dependency
get_db = create_session_dependency(SessionLocal)
```

### With FastAPI

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.get("/items")
async def read_items(db: AsyncSession = Depends(get_db)):
    # Use db session
    result = await db.execute("SELECT * FROM items")
    return result.scalars().all()
```

### Connection Pool Event Handlers

```python
from sqlalchemy_async_session_factory import setup_pool_event_handlers

# Setup event handlers for graceful cleanup
setup_pool_event_handlers(engine)
```

### Manual Session Usage

```python
# Use session directly
async with SessionLocal() as session:
    result = await session.execute("SELECT * FROM items")
    items = result.scalars().all()
```

## API Reference

### `create_async_engine_with_pool(...)`

Create async engine with connection pooling.

**Parameters:**
- `database_url` (str): Database connection URL
- `echo` (bool): Echo SQL queries (default: False)
- `pool_size` (int): Number of connections (default: 5)
- `max_overflow` (int): Max overflow connections (default: 5)
- `pool_timeout` (int): Connection timeout seconds (default: 30)
- `pool_pre_ping` (bool): Test connections (default: True)
- `pool_recycle` (int): Recycle after seconds (default: 300)

**Returns:**
- `AsyncEngine`: Configured engine

### `create_async_session_maker(...)`

Create async session maker.

**Parameters:**
- `engine` (AsyncEngine): Engine instance
- `expire_on_commit` (bool): Expire objects (default: False)

**Returns:**
- `async_sessionmaker[AsyncSession]`: Session maker

### `create_session_dependency(...)`

Create FastAPI session dependency.

**Parameters:**
- `session_maker` (async_sessionmaker): Session maker

**Returns:**
- `Callable`: Dependency function

### `suppress_pool_warnings()`

Suppress connection pool warnings during cleanup.

### `setup_pool_event_handlers(engine)`

Setup event handlers for connection pool.

**Parameters:**
- `engine` (AsyncEngine): Engine instance

## Supported Databases

### PostgreSQL (Recommended)

```python
engine = create_async_engine_with_pool(
    "postgresql+asyncpg://user:pass@localhost:5432/db"
)
```

### SQLite

```python
engine = create_async_engine_with_pool(
    "sqlite+aiosqlite:///./app.db"
)
```

## Dependencies

- `sqlalchemy[asyncio]>=2.0.0`
- `asyncpg>=0.29.0` (PostgreSQL driver)
- `aiosqlite>=0.19.0` (SQLite driver, optional)

## License

MIT
