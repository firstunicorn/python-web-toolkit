# Infrastructure: Data Patterns

Database session management, connection pooling, and DTO mapping patterns.

## Example 10: SQLAlchemy Async Session Management

Async engine creation, session factory, and FastAPI dependency injection.

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool,
    create_async_session_maker,
    create_session_dependency,
    suppress_pool_warnings,
)
from fastapi_config_patterns import BaseDatabaseSettings

# Settings
class Settings(BaseDatabaseSettings):
    pass


settings = Settings()

# Suppress pool warnings during cleanup
suppress_pool_warnings()

# Create engine with connection pooling
engine = create_async_engine_with_pool(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=False,
)

# Create session maker
SessionLocal = create_async_session_maker(engine)

# Create FastAPI dependency
get_db = create_session_dependency(SessionLocal)

# Use in endpoints
app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user
```

## Example 13: DTO Auto-Mapping

Automatic object-to-DTO transformations with field mapping and custom transformations.

```python
from dataclasses import dataclass
from pydantic import BaseModel
from python_dto_mappers import AutoMapper, auto_map, field_transform


# Domain model
@dataclass
class User:
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool


# DTO
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str  # Transformed field
    status: str  # Transformed field


# Method 1: Using AutoMapper class
mapper = AutoMapper(User, UserResponse, exclude={"is_active"})


def full_name_transform(user: User) -> str:
    return f"{user.first_name} {user.last_name}"


def status_transform(user: User) -> str:
    return "active" if user.is_active else "inactive"


mapper.add_transform("full_name", full_name_transform)
mapper.add_transform("status", status_transform)

user = User(1, "user@example.com", "John", "Doe", True)
dto = mapper.map(user)  # UserResponse(id=1, email=..., full_name="John Doe", status="active")


# Method 2: Using @auto_map decorator
@auto_map(User, UserResponse, exclude={"is_active"})
class UserMapper:
    @field_transform("full_name")
    def transform_full_name(self, user: User) -> str:
        return f"{user.first_name} {user.last_name}"

    @field_transform("status")
    def transform_status(self, user: User) -> str:
        return "active" if user.is_active else "inactive"


mapper = UserMapper()
dto = mapper.map(user)
```
