# Quick Start Guide

Get started with Python Web Toolkit in minutes. These 5 essential examples cover the most common workflows.

## Example 1: Basic FastAPI Application

Build a simple API endpoint with validation, sanitization, and error handling.

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Library imports
from python_app_exceptions import ValidationError, BusinessLogicError
from pydantic_response_models import SuccessResponse, ErrorResponse, PaginatedResponse
from sqlalchemy_async_repositories import BaseRepository
from python_technical_primitives.datetime import utc_now, add_days
from postgres_data_sanitizers import sanitize_dict_for_postgres
from python_input_validation import validate_email_format, sanitize_email

app = FastAPI()


# User Repository
class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)


# API Endpoint
@app.post("/users", response_model=SuccessResponse[UserResponse])
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Validate email
    if not validate_email_format(data.email):
        raise HTTPException(400, "Invalid email format")

    # Sanitize input
    email = sanitize_email(data.email)

    # Create user
    user = User(
        email=email,
        created_at=utc_now(),
        expires_at=add_days(utc_now(), 30)
    )

    # Sanitize JSONB data for PostgreSQL
    if data.metadata:
        user.metadata = sanitize_dict_for_postgres(data.metadata)

    # Save to database
    repo = UserRepository(db)
    saved_user = await repo.create(user)

    return SuccessResponse(data=UserResponse.from_orm(saved_user))


# Error handling
@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return ErrorResponse(
        error=exc.message,
        details=[{"field": exc.field, "message": str(exc)}]
    )


@app.exception_handler(BusinessLogicError)
async def business_error_handler(request, exc: BusinessLogicError):
    return ErrorResponse(error=exc.message)
```

## Example 6: Exception Handling Hierarchy

Structured exception management for clear error communication.

```python
from python_app_exceptions import (
    BaseApplicationException,
    ValidationError,
    BusinessLogicError,
    RetryExhaustedException
)

def create_user(email: str, age: int):
    # Validation errors
    if '@' not in email:
        raise ValidationError("email", email, "Invalid format")

    # Business rule violations
    if age < 18:
        raise BusinessLogicError(
            "user_must_be_adult",
            details=f"User is {age} years old"
        )

    # Success
    return {"email": email, "age": age}


# Catch specific exceptions
try:
    user = create_user("invalid", 16)
except ValidationError as e:
    print(f"Validation failed: {e.field} - {e.message}")
except BusinessLogicError as e:
    print(f"Business rule violated: {e.message}")
except BaseApplicationException as e:
    print(f"Application error: {e.message}")
```

## Example 8: Complete FastAPI Setup with Middleware

Production-ready FastAPI setup with CORS, error handlers, lifespan, and health checks.

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import (
    setup_cors_middleware,
    setup_error_handlers,
    create_lifespan_manager,
    create_health_check_endpoint,
)
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings
from python_structlog_config import configure_for_production
from python_app_exceptions import BaseApplicationException

# Configure structured logging
configure_for_production(service_name="my-api", version="1.0.0")


# Settings
class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "My API"
    secret_key: str


settings = Settings()


# Lifespan management
async def on_startup():
    print(f"{settings.app_name} starting...")


async def on_shutdown():
    print(f"{settings.app_name} shutting down...")


lifespan = create_lifespan_manager(
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    service_name=settings.app_name,
    service_version="1.0.0",
)

# Create app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

# Setup middleware
setup_cors_middleware(
    app,
    allowed_origins=settings.allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    max_age=settings.cors_max_age,
)

# Setup error handlers
setup_error_handlers(app, BaseApplicationException)

# Health check
health_check = create_health_check_endpoint(
    service_name=settings.app_name,
    version="1.0.0",
    additional_checks={"database": "connected"},
)
app.get("/health")(health_check)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}!"}
```

## Example 10: SQLAlchemy Async Session Management

Database connection pooling and FastAPI session dependencies.

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

## Example 15: Complete Backend Application

Full backend integrating all 16 libraries - middleware, database, CQRS, outbox, and more.

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

# Infrastructure setup
from fastapi_middleware_toolkit import (
    setup_cors_middleware,
    setup_error_handlers,
    create_lifespan_manager,
)
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings
from sqlalchemy_async_session_factory import (
    create_async_engine_with_pool,
    create_async_session_maker,
    create_session_dependency,
)
from python_structlog_config import configure_for_production, get_logger
from python_cqrs_dispatcher import CQRSDispatcher

# Domain layer
from python_app_exceptions import ValidationError, BusinessLogicError
from pydantic_response_models import SuccessResponse, ErrorResponse
from sqlalchemy_async_repositories import BaseRepository
from python_dto_mappers import AutoMapper

# CQRS
from python_cqrs_core import ICommand, ICommandHandler

# Outbox
from python_outbox_core import IOutboxEvent, IOutboxRepository

# Configure logging
configure_for_production(service_name="order-api", version="1.0.0")
logger = get_logger(__name__)


# Settings
class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "Order API"


settings = Settings()

# Database
engine = create_async_engine_with_pool(settings.database_url, pool_size=10)
SessionLocal = create_async_session_maker(engine)
get_db = create_session_dependency(SessionLocal)


# Lifespan
async def on_startup():
    logger.info("Order API starting")


lifespan = create_lifespan_manager(on_startup=on_startup, service_name="order-api")

# App
app = FastAPI(title=settings.app_name, lifespan=lifespan)
setup_cors_middleware(app, allowed_origins=settings.allowed_origins)
setup_error_handlers(app, BusinessLogicError)


# Domain: Command
class CreateOrderCommand(ICommand):
    customer_id: str
    total: float


class CreateOrderCommandHandler(ICommandHandler[CreateOrderCommand, int]):
    def __init__(self, db: AsyncSession, outbox: IOutboxRepository):
        self.db = db
        self.outbox = outbox

    async def handle(self, command: CreateOrderCommand) -> int:
        # Create order
        order = Order(customer_id=command.customer_id, total=command.total)
        self.db.add(order)

        # Create outbox event (transactional)
        event = OrderCreatedEvent(
            aggregate_id=str(order.id),
            payload={"customer_id": command.customer_id, "total": command.total},
        )
        await self.outbox.save(event)

        await self.db.commit()
        logger.info("Order created", order_id=order.id, total=command.total)
        return order.id


# API
class CreateOrderRequest(BaseModel):
    customer_id: str
    total: float


@app.post("/orders", response_model=SuccessResponse[dict])
async def create_order(
    request: CreateOrderRequest,
    db: AsyncSession = Depends(get_db),
):
    # Validate
    if request.total <= 0:
        raise HTTPException(400, "Total must be positive")

    # Execute command
    command = CreateOrderCommand(
        customer_id=request.customer_id,
        total=request.total,
    )
    outbox = OutboxRepository(db)
    handler = CreateOrderCommandHandler(db, outbox)
    order_id = await handler.handle(command)

    return SuccessResponse(
        data={"order_id": order_id},
        message="Order created successfully",
    )
```

## Next Steps

Explore more examples:
- [All Examples](README.md) - Complete catalog organized by use case
- [Domain Layer Examples](domain/) - Business logic, data patterns, utilities
- [Infrastructure Examples](infrastructure/) - APIs, logging, database, CQRS, messaging
