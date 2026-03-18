# SQLAlchemy Async Repositories

**Async repository pattern with hybrid pagination approach.**

## 🎯 Features

### ✅ Basic CRUD (Native SQLAlchemy - Fast!)
- `get_by_id()` - Get entity by ID
- `create()` - Create new entity
- `update()` - Update existing entity
- `delete()` - Delete entity
- `get_all()` - Get all entities with simple pagination
- `exists()` - Check if entity exists
- `count()` - Count total entities

### ⚡ Advanced Pagination (Hybrid Approach)
- **FastCRUD Integration:** Uses FastCRUD if installed (battle-tested, feature-rich)
- **Native Fallback:** Falls back to native SQLAlchemy (zero dependencies)
- **Type-Safe Filtering:** `FilterSpec` with operators (eq, ne, gt, gte, lt, lte, in, like, ilike)
- **Multi-Field Sorting:** `SortSpec` with asc/desc
- **Rich Metadata:** Total count, pages, has_next, has_prev

## 📦 Installation

### Basic (Native SQLAlchemy only):
```bash
pip install sqlalchemy-async-repositories
```

### With FastCRUD (Recommended):
```bash
pip install sqlalchemy-async-repositories[fastcrud]
```

## 📋 Prerequisites

Before using this library, you need to set up your SQLAlchemy 2.0 models and async session.

### 1. Define Your SQLAlchemy Model

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

class User(Base):
    """Example: User entity."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

### 2. Set Up Async Database Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Create async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/dbname",
    echo=True  # Set to False in production
)

# Create session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Get session
async with async_session() as session:
    # Use session here
    pass
```

**💡 Tip:** For FastAPI, use dependency injection:

```python
from fastapi import Depends

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# In your route
@app.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session, User)
    return await repo.get_by_id(user_id)
```

## 🚀 Usage

### Basic CRUD

```python
from sqlalchemy_async_repositories import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

# Step 1: Define repository for your model
class UserRepository(BaseRepository[User]):
    """
    Repository for User entity.

    Generic type [User]:
    - Provides IDE autocomplete and type hints
    - Ensures type safety (mypy/pyright)
    - No runtime overhead
    """
    pass

# Step 2: Initialize repository
# Parameters:
#   - session: AsyncSession (from SQLAlchemy)
#   - User: Your SQLAlchemy model class
repo = UserRepository(session, User)

# Step 3: Use CRUD methods
# Get by ID
user = await repo.get_by_id(123)  # Returns: Optional[User]

# Create
new_user = User(email="user@example.com", name="John Doe")
created = await repo.create(new_user)  # Returns: User

# Update
user.is_active = False
updated = await repo.update(user)  # Returns: User

# Delete
deleted = await repo.delete(123)  # Returns: bool

# Check existence
exists = await repo.exists(123)  # Returns: bool

# Count all
total = await repo.count()  # Returns: int
```

### Advanced Pagination

```python
from sqlalchemy_async_repositories import FilterSpec, SortSpec
from datetime import datetime, timedelta

yesterday = datetime.utcnow() - timedelta(days=1)

# Paginated query with filters and sorting
result = await repo.find_paginated(
    page=1,
    page_size=10,
    filters=[
        FilterSpec(field="is_active", operator="eq", value=True),
        FilterSpec(field="created_at", operator="gt", value=yesterday),
        FilterSpec(field="email", operator="like", value="example.com")
    ],
    sort=[
        SortSpec(field="created_at", direction="desc"),
        SortSpec(field="name", direction="asc")
    ]
)

# Access results
print(f"Total: {result.total}")
print(f"Page: {result.page}/{result.pages}")
print(f"Has next: {result.has_next}")

for user in result.items:
    print(f"{user.name} - {user.email}")
```

### Filter Operators

```python
FilterSpec(field="age", operator="eq", value=18)       # Equal
FilterSpec(field="age", operator="ne", value=18)       # Not equal
FilterSpec(field="age", operator="gt", value=18)       # Greater than
FilterSpec(field="age", operator="gte", value=18)      # Greater than or equal
FilterSpec(field="age", operator="lt", value=18)       # Less than
FilterSpec(field="age", operator="lte", value=18)      # Less than or equal
FilterSpec(field="status", operator="in", value=["active", "pending"])  # In list
FilterSpec(field="email", operator="like", value="example.com")  # Like (case-sensitive)
FilterSpec(field="email", operator="ilike", value="example.com") # iLike (case-insensitive)
```

### Check FastCRUD Availability

```python
from sqlalchemy_async_repositories import has_fastcrud

if has_fastcrud():
    print("Using FastCRUD for pagination")
else:
    print("Using native SQLAlchemy for pagination")
```

## 🏗️ Architecture

### Hybrid Approach

```
┌─────────────────────────────────────────┐
│         BaseRepository                   │
│                                          │
│  Basic CRUD:                             │
│  ✅ Native SQLAlchemy (always)          │
│     - Fast                               │
│     - Simple                             │
│     - No dependencies                    │
│                                          │
│  Pagination/Filtering:                   │
│  ⚡ FastCRUD (if installed)              │
│     - Battle-tested                      │
│     - Feature-rich                       │
│     - Advanced joins                     │
│                                          │
│  🔄 Native SQLAlchemy (fallback)        │
│     - Zero dependencies                  │
│     - Simple implementation              │
│     - Type-safe                          │
└─────────────────────────────────────────┘
```

### Why Hybrid?

1. **Flexibility:** Works with or without FastCRUD
2. **Performance:** Native SQLAlchemy for basic operations
3. **Battle-tested:** FastCRUD for complex pagination when available
4. **Zero Lock-in:** Can switch between implementations
5. **Clean API:** Same interface regardless of backend

## 🧪 Testing

```python
import pytest
from sqlalchemy_async_repositories import BaseRepository, FilterSpec, SortSpec

@pytest.mark.asyncio
async def test_pagination(session):
    """Test pagination with filters."""
    repo = UserRepository(session, User)

    result = await repo.find_paginated(
        page=1,
        page_size=5,
        filters=[FilterSpec(field="is_active", operator="eq", value=True)]
    )

    assert result.total >= 0
    assert len(result.items) <= 5
    assert result.page == 1
```

## 📚 Documentation

For complete documentation on the repository pattern and DDD architecture, see:
- `architecture/01_ARCHITECTURE_BASICS.md` - Repository pattern basics
- `architecture/02_ARCHITECTURE_STRUCTURE.md` - Where repositories fit

## 🤝 Related Packages

- `python-app-exceptions` - Exception handling
- `python-domain-primitives` - Domain entities and value objects
- `python-cqrs-core` - CQRS pattern implementation

## 🏗️ Design Patterns

This library uses **6 complementary design patterns** for flexibility and maintainability:

| Pattern | Purpose | Where |
|---------|---------|-------|
| **Repository** | Abstract data access | `base.py` |
| **CQRS with use-cases** | Separate read/write | `use_cases/` |
| **Strategy** | Swap pagination backends | `pagination/strategies/` |
| **Factory** | Create strategies | `strategy_factory.py` |
| **Protocol (PEP 544)** | Type-safe interfaces | `IPaginationStrategy` |
| **Composition** | Build from components | Handler delegation |

**Each pattern solves a specific problem** - see [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed explanation, visual diagrams, and trade-off analysis.

### Why Multiple Patterns?

✅ **Repository** - Hides SQLAlchemy details
✅ **CQRS** - Separate read/write, which is must-have for repositories
✅ **Strategy** - Zero lock-in (FastCRUD optional)
✅ **Factory** - Testable strategy selection
✅ **Protocol** - Type safety without inheritance
✅ **Composition** - Flexible, not rigid

**Pattern Philosophy:** "Use patterns when they serve a purpose, not for pattern's sake."

## 📄 License

MIT
