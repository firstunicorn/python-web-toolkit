# Infrastructure: Complete Backend Application

Full backend application integrating all 16 libraries - middleware, database, CQRS, outbox, and more.

## Example 15: Complete Backend Application

Production-ready backend demonstrating integration of all domain and infrastructure libraries.

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

This example demonstrates:
- FastAPI middleware setup (CORS, error handlers, lifespan)
- Pydantic settings with environment variables
- SQLAlchemy async engine and session management
- Structured logging with context
- CQRS command pattern
- Transactional outbox for reliable events
- Repository pattern
- DTO mapping
- Standardized API responses
