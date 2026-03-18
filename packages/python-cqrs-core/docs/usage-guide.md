# Usage Guide

Complete guide to using Python CQRS Core in your applications.

## Commands

Commands represent write operations that modify state.

```python
from python_cqrs_core import BaseCommand, ICommandHandler

class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    async def handle(self, command: CreateUserCommand) -> int:
        # Create user logic
        user_id = await self.user_repository.create(
            name=command.name,
            email=command.email
        )
        return user_id

# Usage
cmd = CreateUserCommand(
    name="John Doe",
    email="john@example.com",
    requested_by="admin"
)
handler = CreateUserHandler()
user_id = await handler.handle(cmd)
```

## Queries

Queries represent read operations that fetch state.

```python
from python_cqrs_core import BaseQuery, IQueryHandler

class GetUserQuery(BaseQuery):
    user_id: int

class GetUserHandler(IQueryHandler[GetUserQuery, User]):
    async def handle(self, query: GetUserQuery) -> User:
        # Fetch user logic
        return await self.user_repository.get(query.user_id)

# Usage
query = GetUserQuery(user_id=1, requested_by="admin")
handler = GetUserHandler()
user = await handler.handle(query)
```

## Paginated Queries

Queries with built-in pagination support.

```python
from python_cqrs_core import PaginatedQuery

class ListUsersQuery(PaginatedQuery):
    status: str = "active"

query = ListUsersQuery(page=2, page_size=20, status="active")
offset = query.offset  # 20
limit = query.page_size  # 20

# Use in database query
users = await db.query(User).offset(query.offset).limit(query.page_size).all()
```

## Tracing Fields

All commands and queries include built-in tracing fields for observability:

```python
cmd = CreateUserCommand(name="John", email="john@example.com")

print(cmd.request_id)       # UUID
print(cmd.correlation_id)   # Optional[UUID]
print(cmd.requested_by)     # Optional[str]
print(cmd.requested_at)     # datetime
```

### Field Details

#### `request_id`
- **Type:** `UUID`
- **Auto-generated:** Yes
- **Purpose:** Unique identifier for this specific command/query
- **Usage:** Track the request through logs and traces

#### `correlation_id`
- **Type:** `Optional[UUID]`
- **Default:** `None`
- **Purpose:** Link related operations across services
- **Usage:** Set to another command's `request_id` to create a trace chain

```python
# Initial command
save_cmd = SaveStateCommand(token="abc123", entity_id=1)
await handler.handle(save_cmd)

# Related command - link them
finalize_cmd = FinalizeSessionCommand(
    token="abc123",
    correlation_id=save_cmd.request_id  # Link to previous operation
)
await handler.handle(finalize_cmd)
```

#### `requested_by`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Purpose:** Identify who initiated the operation
- **Usage:** Audit trail, security, logging

```python
cmd = CreateUserCommand(
    name="Jane",
    email="jane@example.com",
    requested_by="admin@example.com"  # Audit trail
)
```

#### `requested_at`
- **Type:** `datetime`
- **Auto-generated:** Yes (UTC)
- **Purpose:** Timestamp when command/query was created
- **Usage:** Performance monitoring, audit trail

```python
cmd = CreateUserCommand(name="John", email="john@example.com")
duration = (datetime.now(timezone.utc) - cmd.requested_at).total_seconds()
logger.info(f"Command processing took {duration}s")
```

## Complete Example

Here's a complete example showing commands, queries, and handlers working together:

```python
from python_cqrs_core import BaseCommand, BaseQuery, ICommandHandler, IQueryHandler
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

# Domain Model
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

# Command
class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    def __init__(self, repository):
        self.repository = repository
    
    async def handle(self, command: CreateUserCommand) -> int:
        logger.info(
            f"[{command.request_id}] Creating user {command.email} "
            f"requested by {command.requested_by} at {command.requested_at}"
        )
        
        user_id = await self.repository.create(
            name=command.name,
            email=command.email
        )
        
        duration = (datetime.now(timezone.utc) - command.requested_at).total_seconds()
        logger.info(f"[{command.request_id}] User created in {duration}s")
        
        return user_id

# Query
class GetUserQuery(BaseQuery):
    user_id: int

class GetUserHandler(IQueryHandler[GetUserQuery, User]):
    def __init__(self, repository):
        self.repository = repository
    
    async def handle(self, query: GetUserQuery) -> User:
        logger.info(
            f"[{query.request_id}] Fetching user {query.user_id} "
            f"requested by {query.requested_by}"
        )
        
        user = await self.repository.get(query.user_id)
        
        return user

# Usage
async def main():
    # Create user
    create_cmd = CreateUserCommand(
        name="John Doe",
        email="john@example.com",
        requested_by="admin@example.com"
    )
    create_handler = CreateUserHandler(user_repository)
    user_id = await create_handler.handle(create_cmd)
    
    # Fetch user (linked via correlation_id)
    get_query = GetUserQuery(
        user_id=user_id,
        correlation_id=create_cmd.request_id,  # Link to create operation
        requested_by="admin@example.com"
    )
    get_handler = GetUserHandler(user_repository)
    user = await get_handler.handle(get_query)
    
    print(f"Created and fetched user: {user.name}")
```

## Best Practices

### Always Set `requested_by`

```python
# ✅ Good
cmd = CreateUserCommand(
    name="John",
    email="john@example.com",
    requested_by="admin@example.com"
)

# ❌ Bad (no audit trail)
cmd = CreateUserCommand(
    name="John",
    email="john@example.com"
)
```

### Use `correlation_id` for Related Operations

```python
# First operation
create_cmd = CreateUserCommand(name="John", email="john@example.com")
user_id = await handler.handle(create_cmd)

# Related operation - link them
send_email_cmd = SendWelcomeEmailCommand(
    user_id=user_id,
    correlation_id=create_cmd.request_id  # ✅ Trace the relationship
)
await email_handler.handle(send_email_cmd)
```

### Log with `request_id`

```python
async def handle(self, command: CreateUserCommand) -> int:
    logger.info(f"[{command.request_id}] Starting user creation")
    
    try:
        user_id = await self.repository.create(command)
        logger.info(f"[{command.request_id}] User created successfully")
        return user_id
    except Exception as e:
        logger.error(f"[{command.request_id}] Failed to create user: {e}")
        raise
```

### Track Performance

```python
async def handle(self, query: GetUserQuery) -> User:
    start = query.requested_at
    
    user = await self.repository.get(query.user_id)
    
    duration = (datetime.now(timezone.utc) - start).total_seconds()
    metrics.record_query_duration("GetUser", duration)
    
    if duration > 1.0:
        logger.warning(
            f"[{query.request_id}] Slow query: GetUser "
            f"took {duration}s for user_id={query.user_id}"
        )
    
    return user
```

## Next Steps

- See [Why Use BaseQuery/BaseCommand?](why-use-base-classes.md) for design rationale
- See [Observability Integration](observability.md) for OpenTelemetry/Sentry/Prometheus
- See [API Reference](api-reference.md) for complete API documentation
