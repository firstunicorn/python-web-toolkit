# sqlalchemy-async-session-factory

Factory functions for async SQLAlchemy engine and session management with connection pooling.

## Installation

```bash
pip install sqlalchemy-async-session-factory
```

## Public API

| Function | Purpose |
|----------|---------|
| `create_async_engine_with_pool(database_url, ...)` | Create async engine with pool config |
| `create_async_session_maker(engine, ...)` | Create `async_sessionmaker` |
| `create_session_dependency(session_maker)` | FastAPI `Depends()` factory |
| `suppress_pool_warnings()` | Suppress pool warnings during shutdown |
| `setup_pool_event_handlers(engine)` | Pool event handlers (monitoring) |

## Usage

```python
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool,
    create_async_session_maker,
    create_session_dependency,
)

engine = create_async_engine_with_pool("postgresql+asyncpg://...")
session_maker = create_async_session_maker(engine)
get_session = create_session_dependency(session_maker)

# FastAPI dependency injection
@app.get("/users")
async def list_users(session=Depends(get_session)):
    ...
```
