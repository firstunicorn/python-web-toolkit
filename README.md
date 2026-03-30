# Python Web Toolkit

[![Tests](https://img.shields.io/badge/tests-331%20passing-brightgreen)](https://github.com/firstunicorn/python-web-toolkit/actions)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validate Dependencies](https://github.com/firstunicorn/python-web-toolkit/actions/workflows/validate-dependencies.yml/badge.svg)](https://github.com/firstunicorn/python-web-toolkit/actions/workflows/validate-dependencies.yml)

Comprehensive Python web development toolkit organized as a monorepo with 17 independent micro-libraries.

<details>
<summary><b>Extracted from production backend</b></summary>

**From `backend/src/shared/`:** exceptions/ (base_exceptions.py, business_errors.py, validation.py, retry_logic.py), repositories/ (interfaces.py, base.py), primitives/ (datetime_operations.py, string_operations.py, specification patterns), validators/ (postgres escape/sanitize/validate, string_validators.py), schemas/ (common_fields.py, field_mixins.py), api_contracts/ (common_fields.py, common_responses_dto.py), business_validation/input_validators.py, business_sanitization/input_sanitizers.py. **Total:** ~500 LOC production + 1,085 LOC tests (yes, there are a lot of rigorous tests, because it is shared, universal code).

</details>

**Key benefit:** Those extracted ~500 lines in libraries can now be reused across multiple projects, saving ~65 lines per each use for each micro-library; sixty lines don't sound like much, but imagine if you use several of them and do that a few times per project - it can easily go up to 1000 lines of code in just one project. Add on top of that tests and maintenance - you end up saving hours if not days of work. Bonus is flexibility: use and keep only what you really need right now (with near zero dependencies). We will add new cases and stats and extend the list of components in the future.

<details>
<summary><b>Examples and real cases of estimated LOC saved per app:</b></summary>
(those was ultra small apps)

**flow_engine:** ~200-250 lines saved (most repositories, CQRS, exceptions)

**token_generator:** ~150-200 lines saved (full CQRS + events + specifications)

**file_management:** ~100-150 lines saved (infrastructure exceptions + repositories)

**flow_engine saved the most LOC** due to its complex multi-repository architecture.

</details>

## What each micro-library solves

<details>
<summary><b>python-input-validation</b> — email/string validation</summary>

BEFORE (without library):
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize(text: str, max_len: int) -> str:
    return text.strip()[:max_len].replace('\x00', '')
```

AFTER (using library):
```python
from python_input_validation import validate_email_format, sanitize_text_input

valid = validate_email_format(email)
safe = sanitize_text_input(raw_input, max_length=255)
```
</details>

<details>
<summary><b>sqlalchemy-async-repositories</b> — generic async CRUD</summary>

BEFORE (without library):
```python
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, page: int, size: int) -> list[User]:
    result = await db.execute(select(User).offset((page-1)*size).limit(size))
    return list(result.scalars().all())
# repeat for every entity...
```

AFTER (using library):
```python
from sqlalchemy_async_repositories import BaseRepository, FilterSpec

repo = BaseRepository(session, User)
user = await repo.get_by_id(1)
page = await repo.find_paginated(page=1, filters=[FilterSpec("status", "eq", "active")])
```
</details>

<details>
<summary><b>sqlalchemy-async-session-factory</b> — async engine/session setup</summary>

BEFORE (without library):
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
    DATABASE_URL, echo=False, pool_size=5,
    max_overflow=10, pool_recycle=3600,
    pool_pre_ping=True,
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session
```

AFTER (using library):
```python
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool, create_async_session_maker, create_session_dependency,
)

engine = create_async_engine_with_pool("postgresql+asyncpg://...")
SessionLocal = create_async_session_maker(engine)
get_db = create_session_dependency(SessionLocal)
```
</details>

<details>
<summary><b>python-structlog-config</b> — structured logging presets</summary>

BEFORE (without library):
```python
import logging
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),  # dev only, must swap for prod
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)
logger = structlog.get_logger()
```

AFTER (using library):
```python
from python_structlog_config import configure_for_development, get_logger

configure_for_development("my-api")
logger = get_logger(__name__)
```
</details>

<details>
<summary><b>fastapi-middleware-toolkit</b> — middleware one-liner setup</summary>

BEFORE (without library):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.exception_handler(Exception)
async def handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})

@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield
    await close_db()
```

AFTER (using library):
```python
from fastapi_middleware_toolkit import setup_cors_middleware, setup_error_handlers, create_lifespan_manager

setup_cors_middleware(app, ["http://localhost:3000"])
setup_error_handlers(app)
app = FastAPI(lifespan=create_lifespan_manager(on_startup=init_db, on_shutdown=close_db))
```
</details>

<details>
<summary><b>gridflow-python-mediator</b> — mediator with pipeline behaviors</summary>

BEFORE (without library):
```python
# every handler call needs manual logging, timing, validation
import time
logger.info(f"Handling {command}")
start = time.time()
validate(command)
result = await handler.handle(command)
logger.info(f"Done in {time.time() - start:.2f}s")
```

AFTER (using library):
```python
from gridflow_python_mediator import Mediator, LoggingBehavior, TimingBehavior

mediator = Mediator()
mediator.add_pipeline_behavior(LoggingBehavior().handle)
mediator.add_pipeline_behavior(TimingBehavior().handle)
result = await mediator.send(command)  # logging + timing automatic
```
</details>

<details>
<summary><b>python-cqrs-core</b> — command/query separation</summary>

BEFORE (without library):
```python
# business logic mixed into route handler
@app.post("/users")
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if await db.execute(select(User).where(User.email == data.email)):
        raise HTTPException(409)
    user = User(**data.dict())
    db.add(user)
    await db.commit()
    return user
```

AFTER (using library):
```python
from python_cqrs_core import BaseCommand, ICommandHandler

class CreateUser(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUser, User]):
    async def handle(self, command: CreateUser) -> User: ...

# route is just a thin adapter, logic lives in handler
```
</details>

<details>
<summary><b>python-dto-mappers</b> — auto DTO mapping</summary>

BEFORE (without library):
```python
def to_dto(user: UserORM) -> UserDTO:
    return UserDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at.isoformat() if user.created_at else None,
    )
# repeat for every entity...
```

AFTER (using library):
```python
from python_dto_mappers import AutoMapper

mapper = AutoMapper(UserORM, UserDTO)
mapper.add_transform("created_at", lambda dt: dt.isoformat() if dt else None)
dto = mapper.map(user_orm)  # fields matched by name automatically
```
</details>

<details>
<summary><b>fastapi-config-patterns</b> — typed settings from env</summary>

BEFORE (without library):
```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
PORT = int(os.getenv("PORT", "8000"))
# no validation, no type safety, silent failures on typos
```

AFTER (using library):
```python
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings

class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "my-api"
# debug, port, cors_origins, database_url — typed, validated, from .env
```
</details>

<details>
<summary><b>python-app-exceptions</b> — typed exception hierarchy</summary>

BEFORE (without library):
```python
# scattered across codebase, no structure
raise Exception("User not found")
# caller has no idea what to catch
try:
    get_user(id)
except Exception:  # catches everything, even bugs
    return 404
```

AFTER (using library):
```python
from python_app_exceptions import BusinessLogicError, ValidationError

raise BusinessLogicError("duplicate_email")
raise ValidationError("email", "not@valid")
# caller catches exactly what they need
```
</details>

<details>
<summary><b>python-infrastructure-exceptions</b> — infra failure types</summary>

BEFORE (without library):
```python
try:
    await db.execute(query)
except Exception as e:
    if "connection" in str(e).lower():
        # guess if it's DB, cache, or queue...
        log.error(f"Something failed: {e}")
```

AFTER (using library):
```python
from python_infrastructure_exceptions import DatabaseError, CacheError

raise DatabaseError("pool exhausted", query="SELECT ...")
raise CacheError("Redis connection refused")
# each infra layer has its own exception — no guessing
```
</details>

<details>
<summary><b>python-technical-primitives</b> — datetime/text/specification</summary>

BEFORE (without library):
```python
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)
expiry = now + timedelta(days=7)
is_expired = datetime.now(timezone.utc) > expiry
iso = now.isoformat()
```

AFTER (using library):
```python
from python_technical_primitives.datetime import utc_now, add_days, is_expired, to_iso_string

now = utc_now()
expiry = add_days(now, 7)
expired = is_expired(expiry)
iso = to_iso_string(now)
```
</details>

<details>
<summary><b>postgres-data-sanitizers</b> — null chars/surrogates</summary>

BEFORE (without library):
```python
# crashes on insert: "invalid byte sequence for encoding UTF8: 0x00"
data = {"bio": user_input}  # may contain \x00 or surrogates
await session.execute(insert(User).values(**data))  # 💥 DataError
```

AFTER (using library):
```python
from postgres_data_sanitizers import sanitize_dict_for_postgres

safe = sanitize_dict_for_postgres({"bio": user_input})
await session.execute(insert(User).values(**safe))  # null chars stripped
```
</details>

<details>
<summary><b>python-cqrs-dispatcher</b> — auto command/query routing</summary>

BEFORE (without library):
```python
# manual wiring in every endpoint
if isinstance(request, CreateUserCommand):
    result = await create_user_handler.handle(request)
elif isinstance(request, GetUserQuery):
    result = await get_user_handler.handle(request)
# grows with every new command/query...
```

AFTER (using library):
```python
from python_cqrs_dispatcher import CQRSDispatcher

dispatcher = CQRSDispatcher()
dispatcher.register_command_handler(CreateUserCommand, CreateUserHandler())
dispatcher.register_query_handler(GetUserQuery, GetUserHandler())
result = await dispatcher.send_command(cmd)  # auto-routes by type
```
</details>

<details>
<summary><b>pydantic-response-models</b> — uniform API responses</summary>

BEFORE (without library):
```python
# inconsistent response shapes across endpoints
return {"data": user, "status": "ok"}           # endpoint A
return {"result": users, "count": len(users)}    # endpoint B
return {"error": "not found", "code": 404}       # endpoint C
```

AFTER (using library):
```python
from pydantic_response_models import SuccessResponse, ErrorResponse, PaginatedResponse

return SuccessResponse(data=user)
return PaginatedResponse(items=users, total=100, page=1, page_size=10, pages=10)
return ErrorResponse(error="Not found", code=404)
```
</details>

<details>
<summary><b>python-outbox-core</b> — transactional outbox pattern</summary>

BEFORE (without library):
```python
# event lost if app crashes between commit and publish
await session.commit()
await kafka.publish({"type": "user.created", "data": user.dict()})  # 💥 crash here = lost event
```

AFTER (using library):
```python
from python_outbox_core import IOutboxEvent, CloudEventsFormatter

class UserCreated(IOutboxEvent):
    event_type: str = "user.created"
    user_id: int

# event saved in same DB transaction — published later by outbox worker
# zero lost events, even on crash
```
</details>

<details>
<summary><b>python-domain-events</b> — in-process domain event dispatch</summary>

BEFORE (without library):
```python
# ad-hoc event handling scattered across services
class UserService:
    def create_user(self, data):
        user = self.repo.save(data)
        self.email_service.send_welcome(user)      # tight coupling
        self.cache_service.invalidate("users")      # more coupling
        self.activity_log.record("user_created")    # even more
```

AFTER (using library):
```python
from python_domain_events import BaseDomainEvent, InProcessEventDispatcher

class UserCreated(BaseDomainEvent):
    event_type: str = "user.created"
    user_id: int

dispatcher = InProcessEventDispatcher()
dispatcher.register(UserCreated, SendWelcomeEmailHandler())
dispatcher.register(UserCreated, InvalidateCacheHandler())
await dispatcher.dispatch(UserCreated(user_id=42))
```
</details>

### Summary

| Library | BEFORE (without) | AFTER (with) |
|---------|-------------------|--------------|
| **python-input-validation** | Manual regex for emails, hand-rolled sanitizers | `validate_email()`, `sanitize_string()` — tested, reusable |
| **sqlalchemy-async-repositories** | Raw SQL or repeated CRUD per entity | `AsyncRepository[Entity]` — generic CRUD + filtering |
| **sqlalchemy-async-session-factory** | Copy-paste async engine + session boilerplate per project | `create_engine()` / `create_session()` — one-liner setup |
| **python-structlog-config** | Raw `print()` or inconsistent logging setup | `configure_logging("dev")` — JSON in prod, colored in dev |
| **fastapi-middleware-toolkit** | Manual CORS / error handler / lifespan wiring | `setup_middleware(app)` — one call configures everything |
| **gridflow-python-mediator** | Direct handler calls, no cross-cutting concerns | `mediator.send(cmd)` with pipeline behaviors (logging, validation) |
| **python-cqrs-core** | Business logic mixed into route handlers | `Command` / `Query` objects enforce read-write separation |
| **python-dto-mappers** | Manual `dict → DTO` conversion in every endpoint | `@auto_map` decorator — zero boilerplate mapping |
| **fastapi-config-patterns** | Scattered `os.getenv()` calls, no validation | Pydantic `Settings` classes with type-safe env loading |
| **python-app-exceptions** | Bare `raise Exception("...")` scattered everywhere | Typed hierarchy: `NotFoundError`, `ValidationError`, `ConflictError` |
| **python-infrastructure-exceptions** | Generic `Exception` for DB/cache/storage failures | `DatabaseError`, `CacheError`, `StorageError` with context |
| **python-technical-primitives** | Re-implementing text/datetime/spec-pattern in every project | Import and use — `slugify()`, `DateRange`, `Specification` |
| **postgres-data-sanitizers** | Crashes on null chars / surrogates in Postgres writes | Auto-strip before insert — zero silent data corruption |
| **python-cqrs-dispatcher** | Wiring commands to handlers manually each time | Auto-dispatch: register handler once, dispatcher routes |
| **pydantic-response-models** | Inconsistent API response shapes across endpoints | `ApiResponse[T]`, `PaginatedResponse[T]` — uniform contract |
| **python-domain-events** | Ad-hoc event handling, tight coupling to side-effects | `InProcessEventDispatcher` — register/dispatch with tracing |
| **python-outbox-core** | Lost events on crash / inconsistent event publishing | Transactional outbox — events saved atomically with data |

## Project Structure

This toolkit is designed to be integrated into your project as a **subfolder**:

```
your-project/
├── python-web-toolkit/          # This toolkit (clone/copy here)
│   ├── packages/
│   │   ├── python-app-exceptions/
│   │   ├── pydantic-response-models/
│   │   └── ... (14 more packages)
│   ├── pyproject.toml           # Workspace config
│   └── README.md
├── your-app/                    # Your application code
├── tests/
└── pyproject.toml               # Your project config
```

**Integration options:**
1. **Git submodule**: `git submodule add <repo-url> python-web-toolkit`
2. **Direct clone**: `git clone <repo-url> python-web-toolkit`
3. **Copy**: Download and place in your project

All installation commands assume `python-web-toolkit` is a **subfolder** in your project root.

**All commands below assume you're running from your project root** (where `python-web-toolkit/` folder is located).

## Architecture

This toolkit follows **microservices principles at the library level**:
- Each package is independently installable
- Packages are modularized as ≤100 lines per file (enforced by development rules)
- Zero or minimal dependencies per package
- Clear separation of concerns

### Dependency Architecture

**Primitives Layer** packages are strictly isolated with no cross-dependencies.

**Domain Layer** packages may depend on Primitives, but not on Application layer.

**Application Layer** packages may have lightweight dependencies:
- Application packages may import from domain and primitives packages
- CQRS/mediator packages integrate together
- All packages remain independently deployable

This layered architecture is enforced via Import Linter (see Architecture Validation section).

## Package Catalog

All packages are **v0.1.0** and independently installable.

### Core Primitives & Utilities (Layer: Primitives)
- **python-technical-primitives** - Text, datetime, and specification pattern utilities
  ```bash
  pip install python-technical-primitives
  ```
- **python-app-exceptions** - Application-level exception hierarchy
  ```bash
  pip install python-app-exceptions
  ```
- **python-infrastructure-exceptions** - Infrastructure exception types (database, cache, storage)
  ```bash
  pip install python-infrastructure-exceptions
  ```
- **python-input-validation** - Email and string validation/sanitization
  ```bash
  pip install python-input-validation
  ```
- **postgres-data-sanitizers** - PostgreSQL data sanitization (null chars, surrogates)
  ```bash
  pip install postgres-data-sanitizers
  ```
- **sqlalchemy-async-session-factory** - Async engine and session factories
  ```bash
  pip install sqlalchemy-async-session-factory
  ```
- **python-structlog-config** - Structured logging configuration presets (dev/prod/test)
  ```bash
  pip install python-structlog-config
  ```

### CQRS & Mediator Pattern (Layer: Domain)
- **python-cqrs-core** - CQRS interfaces (ICommand, IQuery, BaseCommand, BaseQuery)
  ```bash
  pip install python-cqrs-core
  ```
- **gridflow-python-mediator** - Generic mediator with pipeline behaviors
  ```bash
  pip install gridflow-python-mediator
  ```
- **python-cqrs-dispatcher** - CQRS dispatcher integrating commands/queries with mediator
  ```bash
  pip install python-cqrs-dispatcher
  ```

### Data & Mapping (Layer: Domain)
- **python-dto-mappers** - Auto-mapping engine and decorators for DTO transformations
  ```bash
  pip install python-dto-mappers
  ```
- **pydantic-response-models** - Standard API response DTOs using Pydantic (framework-agnostic)
  ```bash
  pip install pydantic-response-models
  ```

### Database & Repository Pattern (Layer: Application)
- **sqlalchemy-async-repositories** - Async repository pattern implementation
  ```bash
  pip install sqlalchemy-async-repositories
  ```

### FastAPI Extensions (Layer: Application)
- **fastapi-config-patterns** - Reusable Pydantic settings classes
  ```bash
  pip install fastapi-config-patterns
  ```
- **fastapi-middleware-toolkit** - FastAPI middleware setup (CORS, error handlers, lifespan)
  ```bash
  pip install fastapi-middleware-toolkit
  ```

### Event-Driven / Outbox Pattern (Layer: Domain)
- **python-outbox-core** - Transactional outbox pattern with CloudEvents formatters
  ```bash
  pip install python-outbox-core
  ```

## Quick Start

### Option 1: Install Entire Workspace (Recommended for Development)

```powershell
# From python-web-toolkit root
poetry install
```

This installs all packages in editable mode with cross-references working automatically.

**Benefits:**
- ✅ One command installs everything
- ✅ Cross-package imports work automatically
- ✅ Shared virtual environment
- ✅ Consistent dependency resolution

### Option 2: Install Individual Packages

```powershell
# Install specific package
cd packages/python-cqrs-core
poetry install

# Run tests
poetry run pytest -v
```

**Use when:** Working on a single package in isolation.

**⚠️ Note:** Some packages have cross-dependencies within the monorepo:
- `python-cqrs-dispatcher` requires `python-cqrs-core` + `gridflow-python-mediator`
- `sqlalchemy-async-repositories` may require specific Python constraints

For packages with cross-dependencies, use **Option 1 (Workspace)** instead.

### Option 3: Bulk Install with Script (Recommended for CI/CD)

```powershell
# From python-web-toolkit root
.\scripts\install-all.ps1
```

**Benefits:**
- ✅ Progress tracking per package
- ✅ Error handling and reporting
- ✅ Colored output for quick scanning
- ✅ CI/CD friendly

### Option 4: Quick One-Liner (For Experienced Developers)

```powershell
# From python-web-toolkit root
Get-ChildItem packages -Directory | ForEach-Object {
    cd $_.FullName; poetry install --quiet
}
```

**Use when:** You need a quick manual install without script overhead.

### Option 5: Individual pip Installs (For Custom Setups)

```bash
# Install all packages in editable mode with pip
# Run from your project root (where python-web-toolkit folder is located)
pip install -e ./python-web-toolkit/packages/python-app-exceptions
pip install -e ./python-web-toolkit/packages/pydantic-response-models
pip install -e ./python-web-toolkit/packages/sqlalchemy-async-repositories
pip install -e ./python-web-toolkit/packages/python-technical-primitives
pip install -e ./python-web-toolkit/packages/postgres-data-sanitizers
pip install -e ./python-web-toolkit/packages/python-input-validation
pip install -e ./python-web-toolkit/packages/fastapi-middleware-toolkit
pip install -e ./python-web-toolkit/packages/fastapi-config-patterns
pip install -e ./python-web-toolkit/packages/sqlalchemy-async-session-factory
pip install -e ./python-web-toolkit/packages/python-structlog-config
pip install -e ./python-web-toolkit/packages/python-infrastructure-exceptions
pip install -e ./python-web-toolkit/packages/python-dto-mappers
pip install -e ./python-web-toolkit/packages/python-cqrs-core
pip install -e ./python-web-toolkit/packages/gridflow-python-mediator
pip install -e ./python-web-toolkit/packages/python-cqrs-dispatcher
pip install -e ./python-web-toolkit/packages/python-outbox-core
```

This is **LOCAL installation** from your filesystem, **NOT from PyPI**.

## What `pip install -e` Does:

**`-e`** = **"editable mode"** (also called "development mode")

When you run:
```bash
pip install -e ./python-web-toolkit/packages/python-app-exceptions
```

It means:
1. ✅ Install the package from **LOCAL filesystem** (the `./python-web-toolkit/packages/...` path)
2. ✅ Install in **editable mode** - changes to source code are immediately active (no need to reinstall)
3. ❌ Does **NOT** download from PyPI

## Why Use Editable Mode?

Perfect for **monorepo development**:
- You edit `python-app-exceptions/src/...` files
- Changes are instantly available to other packages or projects
- No need to rebuild/reinstall after every change

## Install from PyPI

If you need these packages **from PyPI**, you'd install normally:
```bash
pip install python-app-exceptions  # Downloads from pypi.org
```

**When to use `-e .`:** You need fine-grained control over which packages to install with pip.

**📝 Note about `-e` flag:**
- `-e` = **editable/development mode** - installs from **LOCAL filesystem**, NOT from PyPI
- Source code changes take effect immediately (no reinstall needed)
- Paths are relative to your project structure
- Perfect for monorepo development where packages are not yet published or custom modifications required

## Development

### Running All Tests

**Option 1: Workspace (Fastest)**
```powershell
# From python-web-toolkit root
poetry run pytest
```

**Option 2: Test Script with Summary (CI/CD)**
```powershell
.\scripts\test-all.ps1
```
Provides detailed summary with pass/fail counts per package.

**Option 3: Quick One-Liner (Manual)**
```powershell
Get-ChildItem packages -Directory | ForEach-Object {
    cd $_.FullName; poetry run pytest -v --tb=short
}
```

**Option 4: Single Package**
```powershell
cd packages/python-cqrs-core
poetry run pytest -v
```

**Option 5: All Packages with Import Mode (Advanced)**
```bash
# Test all micro-library packages (from your project root)
poetry run pytest python-web-toolkit/packages/ --import-mode=importlib -v
```

**Option 6: Save Test Output to Log**
```powershell
# Save detailed test output (from your project root)
poetry run pytest python-web-toolkit/packages/ --import-mode=importlib -v 2>&1 | Tee-Object -FilePath tests/logs/micro_libs_all.txt
```

### Code Quality Standards

- **Architecture**: OOP, DRY, SOLID principles, Layered Architecture
- **Line limit**: 100 lines per file (absolute maximum: 120)
- **Organization**: Split into sub-modules when approaching limit
- **Test coverage**: Comprehensive unit + property-based tests
- **Import rules**: Enforced via Import Linter (see Architecture section)

### Architecture Validation

**Import Linter** enforces architectural boundaries (122 files, 151 dependencies analyzed):

```powershell
# Check import rules
.\scripts\check-architecture.ps1
# Or directly: poetry run lint-imports

# Run with tests
poetry run pytest && poetry run lint-imports
```

**3 Architectural Contracts (All Passing ✓):**

1. **Primitives Layer Cannot Import Domain/Application** - Bottom layer stays isolated
   - `python-technical-primitives`, `python-app-exceptions`, `python-infrastructure-exceptions`
   - ✗ Cannot import: CQRS, mediator, repositories, FastAPI, DTOs

2. **Domain Layer Cannot Import Application** - Mid layer depends only on primitives
   - `python-cqrs-core`, `gridflow-python-mediator`, `pydantic-response-models`, `python-dto-mappers`
   - ✗ Cannot import: `python-cqrs-dispatcher`, repositories, FastAPI middleware

3. **Core Components Independence** - Prevents circular dependencies
   - `python-cqrs-core` and `gridflow-python-mediator` must not import each other

**Layer Hierarchy:**

| Layer | Position | Packages | Import Rules |
|-------|----------|----------|--------------|
| **Application** | Top | `python-cqrs-dispatcher`<br>`sqlalchemy-async-repositories`<br>`fastapi-middleware-toolkit`<br>`fastapi-config-patterns` | ✅ Can import from any layer |
| **Domain** | Middle | `python-cqrs-core`<br>`gridflow-python-mediator`<br>`pydantic-response-models`<br>`python-dto-mappers`<br>`python-input-validation`<br>`python-outbox-core` | ✅ Can import primitives<br>❌ Cannot import application |
| **Primitives** | Bottom | `python-technical-primitives`<br>`python-app-exceptions`<br>`python-infrastructure-exceptions`<br>`postgres-data-sanitizers`<br>`sqlalchemy-async-session-factory`<br>`python-structlog-config` | ❌ Cannot import domain/application<br>(Fully isolated foundation) |

**Text Summary:**
- **Primitives** (bottom): `python-technical-primitives`, exceptions → Cannot import domain/application
- **Domain** (middle): `python-cqrs-core`, `gridflow-python-mediator`, DTOs → Cannot import application
- **Application** (top): `python-cqrs-dispatcher`, repositories, FastAPI → Can import anything

### Adding a New Package

1. Create package structure:
   ```powershell
   cd packages
   poetry new my-new-package
   ```

2. Add to workspace `pyproject.toml`:
   ```toml
   my-new-package = {path = "packages/my-new-package", develop = true}
   ```

3. Install workspace:
   ```bash
   poetry install
   ```

## Documentation

- [Examples Overview](examples/README.md) - All 15 examples organized by use case
- [Quick Start Guide](examples/QUICK_START.md) - 5 essential examples to get started
- [Domain Layer Examples](examples/domain/) - Business logic and data patterns
- [Infrastructure Examples](examples/infrastructure/) - APIs, database, CQRS, messaging

## Publishing to PyPI

Publishing is automated via GitHub Actions using OpenID Connect trusted publishing (no tokens required).

**Setup (one-time):**
1. Configure trusted publisher at https://test.pypi.org/manage/account/publishing/:
   - PyPI project name: `<package-name>`
   - Owner: `<your-github-username>`
   - Repository name: `python-web-toolkit`
   - Workflow name: `publish-testpypi.yml`
   - Environment name: `testpypi`

2. Repeat for production PyPI at https://pypi.org/manage/account/publishing/ using `publish-pypi.yml` workflow.

**Publishing workflow:**
1. Bump version in package `pyproject.toml` files (e.g., 0.1.0 → 0.1.1)
2. Commit and push changes
3. Run workflow:
   - TestPyPI: Go to Actions → "Publish to TestPyPI" → Run workflow
   - Production: Create GitHub release with version tag (e.g., `v0.1.1`)

**Local testing:**
```powershell
.\scripts\build-all.ps1
```

## License

MIT
