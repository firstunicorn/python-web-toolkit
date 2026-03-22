NOTHING ALLOWED TO BE SKIPPED EXCEPT DIAGRAM AND REALLY DEPRECATED PARTS; EVERYTHING ELSE MUST BE ADAPTED, NOT SKIPED



# Hybrid Repository Architecture
## 🏗️ Architecture Overview
```
┌───────────────────────────────────────────
──────────────────┐
│              Client Code (Your
Application)                 │
│  Example: UserRepository(session,
UserORM)                  │
└────────────────────────┬──────────────────
──────────────────┘
                         │
                         │ uses
                         ▼
┌───────────────────────────────────────────
──────────────────┐
│         BaseRepository (Repository +
Facade Patterns)       │
│  • Facade: Simplifies complex use case
coordination         │
│  • Repository: Abstracts data access
layer                  │
│  • Composition: Delegates to use case
handlers              │
├───────────────────────────────────────────
──────────────────┤
│
Methods:
               │
│  - get_by_id() →
GetByIdHandler                             │
│  - create() →
CreateHandler
  │
│  - find_paginated() →
FindPaginatedHandler                  │
└────────────────────────┬──────────────────
──────────────────┘
                         │
                         │ delegates to
                         ▼
┌───────────────────────────────────────────
──────────────────┐
│              Use Cases (CQRS
Pattern)                       │
│  • Separates read operations (queries)
from writes          │
│  • Each use case in isolated
folder                         │
├───────────────────────────────────────────
──────────────────┤
│  Query Side:           │  Command
Side:                     │
│  - get_by_id/          │  -
create/                         │
│  - get_all/            │  -
update/                         │
│  - exists/             │  -
delete/                         │
│  - count/
│                                     │
│  - find_paginated/
│                                     │
└────────────────────────┬──────────────────
──────────────────┘
                         │
                         │ (focus on
                         find_paginated)
                         ▼
┌───────────────────────────────────────────
──────────────────┐
│     FindPaginatedHandler
(Coordinator)                      │
│  • Pattern: Handler Pattern (executes use
case)             │
│  • Uses: Factory Pattern for strategy
creation              │
│  • Uses: Strategy Pattern for algorithm
delegation          │
├───────────────────────────────────────────
──────────────────┤
│  __init__()
:
      │
│    1. Get strategy from Factory
─────────────┐             │
│
    │             │
│  execute()
:
│             │
│    2. Delegate to strategy.execute()
◄───────┼─────┐      │
└───────────────────────────────────────────
────┼─────┼──────┘
                         │
                             │     │
                         │
                             │     │
        ┌────────────────┴──────────┐
           │     │
        │
        │          │     │
        ▼
        ▼          │     │
┌──────────────────┐
┌──────────────────┐│     │
│ Strategy Factory │      │
IPaginationStrategy (Protocol)
│ (Factory Pattern)│      │  • Type-safe
interface (PEP 544)
├──────────────────┤      │  • No
inheritance needed         │
│  create():       │
└──────────┬───────────────────────┘
│   if FastCRUD:
│◄────────────────┘                │
│     → FastCRUD
│                                  │
│   else:          │
implements      │
│     → Native     │
┌────────────┴───────────┤
└──────────────────┘
│                        │
                             ▼
                                       ▼
              ┌──────────────────────┐
              ┌──────────────────────┐
              │  FastCRUDStrategy    │  │
              NativeStrategy     │
              │  (Strategy Pattern)  │  │
              (Strategy Pattern)  │
              ├──────────────────────┤
              ├──────────────────────┤
              │ Uses FastCRUD lib    │  │
              Uses pure SQLAlchemy │
              │ Battle-tested        │  │
              Zero dependencies    │
              │ Feature-rich         │  │
              Simple & clean       │
              └──────────────────────┘
              └──────────────────────┘
## 🔄 Request Flow
### Basic CRUD (Simple & Fast)
```
Application Code
    │
    ├─> repo.create(entity)
    │       │
    │       └─> Native SQLAlchemy
    │               │
    │               └─> db.add(entity)
    │                   db.flush()
    │                   db.refresh(entity)
    │
    └─> Returns created entity
### Pagination (Hybrid Approach)
```
Application Code
    │
    ├─> repo.find_paginated(page=1, filters=
    [...], sort=[...])
    │       │
    │       ├─> Check: FastCRUD available?
    │       │
    │       ├─── YES ──>
    pagination_fastcrud.py
    │       │               │
    │       │               ├─> Convert
    FilterSpec → FastCRUD format
    │       │               ├─> Convert
    SortSpec → FastCRUD format
    │       │               ├─> Call
    FastCRUD.get_multi()
    │       │               └─> Convert
    result → PaginatedResult
    │       │
    │       └─── NO ──> pagination_native.py
    │                       │
    │                       ├─> Build
    SQLAlchemy query
    │                       ├─> Apply
    filters (WHERE clauses)
    │                       ├─> Count total
    (subquery)
    │                       ├─> Apply
    sorting (ORDER BY)
    │                       ├─> Apply
    pagination (LIMIT/OFFSET)
    │                       └─> Return
    PaginatedResult
    │
    └─> Returns PaginatedResult[T]
            │
            ├─ items: List[T]
            ├─ total: int
            ├─ page: int
            ├─ page_size: int
            ├─ pages: int
            ├─ has_next: bool
            └─ has_prev: bool
## 📦 Module Structure
sqlalchemy-async-repositories/
├── src/sqlalchemy_async_repositories/
│   ├── __init__.py                # Public
API
│   ├── interfaces.py              #
IRepository interface
│   ├── base.py                    #
BaseRepository (main class)
│   │   ├─ Basic CRUD methods      ✅ Always
native
│   │   └─ find_paginated()        ⚡ Hybrid
approach
│   │
│   ├── pagination.py              # Shared
types
│   │   ├─ FilterSpec
│   │   ├─ SortSpec
│   │   ├─ PaginatedResult
│   │   └─ has_fastcrud()
│   │
│   ├── pagination_fastcrud.py     #
FastCRUD implementation
│   │   └─ find_paginated_fastcrud()
│   │
│   └── pagination_native.py       # Native
SQLAlchemy fallback
│       └─ find_paginated_native()
│
├── pyproject.toml
│   ├─ dependencies: sqlalchemy, pydantic
│   └─ optional-dependencies:
│       └─ fastcrud: ["fastcrud>=0.12.0"]
# Optional!
│
├── README.md                      # Usage
guide
├── USAGE_EXAMPLE.py               # Real
code examples
└── ARCHITECTURE.md                # This
file
## 🎯 Design Decisions
### 1. Why Hybrid Approach?
| Aspect | Native Only | FastCRUD Only |
Hybrid (Chosen) |
|--------|-------------|---------------|
-----------------|
| **Dependencies** | ✅ Zero | ❌ Requires
FastCRUD | ✅ Optional |
| **Features** | ⚠️ Basic | ✅ Advanced | ✅
Both |
| **Performance** | ✅ Fast CRUD | ✅ Fast
pagination | ✅ Best of both |
| **Flexibility** | ✅ Full control | ⚠️
Limited | ✅ Maximum |
| **Maintenance** | ⚠️ Write tests | ✅
Battle-tested | ✅ Both |
| **Lock-in** | ✅ None | ❌ FastCRUD API | ✅
None |
### 2. Why Keep Basic CRUD Native?
# Basic CRUD is simple enough - no need for
FastCRUD
async def get_by_id(self, entity_id: Any)
-> Optional[T]:
    # Just 3 lines! Fast, simple, no
    dependencies needed
    result = await self.db.execute(
        select(self.model_class).where(self.
        model_class.id == entity_id)
    )
    return result.scalar_one_or_none()
- ✅ **Fast:** Direct SQLAlchemy - no
overhead
- ✅ **Simple:** Easy to understand and debug
- ✅ **Zero dependencies:** Works without
FastCRUD
- ✅ **Full control:** Can optimize per use
case
### 3. Why Use FastCRUD for Pagination?
# Pagination is complex - FastCRUD handles
edge cases
async def find_paginated(...):
    # FastCRUD handles:
    # - Complex filter combinations
    # - Multi-field sorting
    # - Cursor pagination
    # - JOIN operations
    # - Performance optimization
    # - Edge case handling
    # + Battle-tested in production
- ✅ **Battle-tested:** Used in production
by many teams
- ✅ **Feature-rich:** Advanced filtering,
joins, cursors
- ✅ **Maintained:** Active development and
bug fixes
- ✅ **Optional:** Graceful fallback if not
installed
### 4. Why Maintain Repository Abstraction?
# ❌ BAD: Direct FastCRUD usage (tight
coupling)
crud = FastCRUD(InviteORM)
invites = await crud.get_multi
(db=session, ...)
# ✅ GOOD: Repository abstraction (loose
coupling)
repo = InviteRepository(session, InviteORM)
invites = await repo.find_paginated(...)
- ✅ **Clean Architecture:** Maintains DDD
layers
- ✅ **Testable:** Easy to mock repositories
- ✅ **Flexible:** Can swap implementations
- ✅ **Consistent API:** Same interface
everywhere
## 🔍 Implementation Details
### Filter Conversion
# Our API (type-safe, clean)
FilterSpec(field="age", operator="gte",
value=18)

# FastCRUD format (dict-based)
{"age": {"__gte": 18}}
# Native SQLAlchemy (query builder)
query.where(model_class.age >= 18)
### Sort Conversion
```python
# Our API
SortSpec(field="created_at",
direction="desc")
# FastCRUD format
sort_columns=["created_at"], sort_orders=
["desc"]
# Native SQLAlchemy
query.order_by(desc(model_class.created_at))
```
## 🚀 Performance Characteristics
| Operation | Implementation | Performance |
|-----------|----------------|-------------|
| **get_by_id()** | Native SQLAlchemy | ⚡
~0.5ms |
| **create()** | Native SQLAlchemy | ⚡
~1ms |
| **find_paginated()** (FastCRUD) |
FastCRUD | ⚡ ~5-10ms |
| **find_paginated()** (Native) |
SQLAlchemy | ⚡ ~5-15ms |
*Note: Times are approximate and depend on
query complexity and data volume.*
## 🧪 Testing Strategy
### Unit Tests
```python
@pytest.mark.asyncio
async def test_pagination_with_fastcrud
(db_session):
    """Test pagination using FastCRUD
    backend."""
    if not has_fastcrud():
        pytest.skip("FastCRUD not
        installed")
    repo = InviteRepository(db_session,
    InviteORM)
    result = await repo.find_paginated
    (page=1, page_size=5)
    assert result.total >= 0
    assert len(result.items) <= 5
@pytest.mark.asyncio
async def test_pagination_with_native
(db_session, monkeypatch):
    """Test pagination using native backend
    (fallback)."""
    # Force native implementation
    monkeypatch.setattr
    ('sqlalchemy_async_repositories.
    pagination.HAS_FASTCRUD', False)
    repo = InviteRepository(db_session,
    InviteORM)
    result = await repo.find_paginated
    (page=1, page_size=5)
    assert result.total >= 0
    assert len(result.items) <= 5
## 📊 Migration Path
### From Direct SQLAlchemy
```python
# Before: Manual pagination
query = select(Invite).where(Invite.is_used
== False)
total = await session.scalar(select(func.
count()).select_from(query.subquery()))
query = query.order_by(desc(Invite.
created_at)).offset(offset).limit(limit)
result = await session.execute(query)
invites = result.scalars().all()
# After: Clean repository API
result = await repo.find_paginated(
    page=1,
    page_size=10,
    filters=[FilterSpec(field="is_used",
    operator="eq", value=False)],
    sort=[SortSpec(field="created_at",
    direction="desc")]
)
# ✅ Cleaner, type-safe, reusable
```
### From FastCRUD Direct
```python
# Before: Direct FastCRUD usage
crud = FastCRUD(Invite)
result = await crud.get_multi(db=session,
is_used=False, ...)
# After: Repository with FastCRUD under the
hood
repo = InviteRepository(session, InviteORM)
result = await repo.find_paginated(
    filters=[FilterSpec(field="is_used",
    operator="eq", value=False)]
)
# ✅ Maintains clean architecture, can swap
implementations
```
## 🎓 Best Practices
1. **Use Basic CRUD for simple operations**
   ```python
   invite = await repo.get_by_id(123)  #
   Fast, simple
   ```
2. **Use pagination for list operations**
   ```python
   result = await repo.find_paginated
   (page=1, page_size=10)
   ```
3. **Build domain-specific methods**
   ```python
   class InviteRepository(BaseRepository):
       async def find_active(self, page:
       int):
           return await self.find_paginated(
               page=page,
               filters=[FilterSpec
               (field="is_used",
               operator="eq", value=False)]
           )
   ```
4. **Check FastCRUD availability if needed**
   ```python
   if has_fastcrud():
       # Use advanced features
       pass
   ```
## 📚 References
- [FastCRUD Documentation](https://
benavlabs.github.io/fastcrud/)
- [SQLAlchemy 2.0 Documentation](https://
docs.sqlalchemy.org/en/20/)
- [Repository Pattern (Martin Fowler)]
(https://martinfowler.com/eaaCatalog/
repository.html)