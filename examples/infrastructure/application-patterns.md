# Infrastructure: Application Patterns

CQRS and Mediator patterns for separating read/write operations and adding cross-cutting concerns.

## Example 11: CQRS Pattern with Commands & Queries

Separated read (Query) and write (Command) operations with dedicated handlers.

```python
from dataclasses import dataclass
from python_cqrs_core import ICommand, IQuery, ICommandHandler, IQueryHandler
from python_infrastructure_exceptions import DatabaseError

# Command: Write operation
@dataclass
class CreateUserCommand(ICommand):
    email: str
    name: str


class CreateUserCommandHandler(ICommandHandler[CreateUserCommand, int]):
    def __init__(self, db):
        self.db = db

    async def handle(self, command: CreateUserCommand) -> int:
        user = User(email=command.email, name=command.name)
        self.db.add(user)
        await self.db.commit()
        return user.id


# Query: Read operation
@dataclass
class GetUserByIdQuery(IQuery):
    user_id: int


class GetUserByIdQueryHandler(IQueryHandler[GetUserByIdQuery, User]):
    def __init__(self, db):
        self.db = db

    async def handle(self, query: GetUserByIdQuery) -> User:
        result = await self.db.execute(
            select(User).where(User.id == query.user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise DatabaseError(f"User {query.user_id} not found")
        return user


# Usage
command = CreateUserCommand(email="user@example.com", name="John Doe")
handler = CreateUserCommandHandler(db)
user_id = await handler.handle(command)

query = GetUserByIdQuery(user_id=user_id)
query_handler = GetUserByIdQueryHandler(db)
user = await query_handler.handle(query)
```

## Example 12: Mediator with Pipeline Behaviors

Generic mediator with logging, timing, and validation behaviors for cross-cutting concerns.

```python
from gridflow_python_mediator import Mediator
from gridflow_python_mediator.behaviors import (
    LoggingBehavior,
    TimingBehavior,
    ValidationBehavior,
)
from pydantic import BaseModel, field_validator

# Create mediator
mediator = Mediator()

# Add pipeline behaviors (execute in order)
mediator.add_pipeline_behavior(LoggingBehavior().handle)
mediator.add_pipeline_behavior(TimingBehavior().handle)
mediator.add_pipeline_behavior(ValidationBehavior().handle)


# Pydantic request with validation
class CreateOrderRequest(BaseModel):
    user_id: int
    amount: float

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v


# Handler
class CreateOrderHandler:
    async def handle(self, request: CreateOrderRequest):
        return {"order_id": 123, "amount": request.amount}


# Register handler
mediator.register(CreateOrderRequest, CreateOrderHandler())

# Send request (logs, times, validates automatically)
request = CreateOrderRequest(user_id=1, amount=99.99)
result = await mediator.send(request)
# Logs output:
# INFO: Handling request request_type=CreateOrderRequest
# INFO: Request timing request_type=CreateOrderRequest duration_ms=5
```
