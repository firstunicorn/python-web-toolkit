# API Reference

## Interfaces

### `ICommand`

Marker interface for commands (write operations).

Commands represent intentions to change state in the system.

**Usage:**
```python
from python_cqrs_core import ICommand

class MyCommand(ICommand):
    pass
```

### `ICommandHandler[TCommand, TResult]`

Handler interface for commands.

**Type Parameters:**
- `TCommand`: The command type this handler processes
- `TResult`: The return type of the handler

**Methods:**

#### `async handle(command: TCommand) -> TResult`

Process the command and return a result.

**Parameters:**
- `command`: The command to process

**Returns:**
- Result of the command execution

**Example:**
```python
from python_cqrs_core import ICommandHandler, BaseCommand

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
```

### `IQuery`

Marker interface for queries (read operations).

Queries represent requests to read state from the system.

**Usage:**
```python
from python_cqrs_core import IQuery

class MyQuery(IQuery):
    pass
```

### `IQueryHandler[TQuery, TResult]`

Handler interface for queries.

**Type Parameters:**
- `TQuery`: The query type this handler processes
- `TResult`: The return type of the handler

**Methods:**

#### `async handle(query: TQuery) -> TResult`

Process the query and return a result.

**Parameters:**
- `query`: The query to process

**Returns:**
- Result of the query execution

**Example:**
```python
from python_cqrs_core import IQueryHandler, BaseQuery

class GetUserQuery(BaseQuery):
    user_id: int

class GetUserHandler(IQueryHandler[GetUserQuery, User]):
    async def handle(self, query: GetUserQuery) -> User:
        return await self.user_repository.get(query.user_id)
```

## Base Classes

### `BaseCommand`

Base command with tracing and audit fields.

All commands should extend this class to gain automatic observability features.

**Inheritance:**
```python
BaseCommand(BaseModel, ICommand)
```

**Fields:**

#### `request_id: UUID`
- **Type:** `UUID`
- **Default:** Auto-generated via `uuid4()`
- **Description:** Unique request identifier for this command
- **Usage:** Track this specific command execution through logs and traces

#### `correlation_id: Optional[UUID]`
- **Type:** `Optional[UUID]`
- **Default:** `None`
- **Description:** Correlation ID for distributed tracing
- **Usage:** Link related commands/queries across service boundaries

#### `requested_by: Optional[str]`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Description:** User or system that initiated the command
- **Usage:** Audit trail - track who performed the action

#### `requested_at: datetime`
- **Type:** `datetime`
- **Default:** Auto-generated via `datetime.now(timezone.utc)`
- **Description:** Timestamp when command was created
- **Usage:** Audit trail and performance monitoring

**Configuration:**
- `frozen=True`: Commands are immutable after creation

**Example:**
```python
from python_cqrs_core import BaseCommand

class CreateUserCommand(BaseCommand):
    name: str
    email: str

# Usage
cmd = CreateUserCommand(
    name="John Doe",
    email="john@example.com",
    requested_by="admin@example.com"
)

print(cmd.request_id)      # UUID('550e8400-e29b-41d4-a716-446655440000')
print(cmd.requested_by)    # "admin@example.com"
print(cmd.requested_at)    # datetime(2026, 2, 26, 10, 30, 45, tzinfo=timezone.utc)
```

### `BaseQuery`

Base query with tracing fields.

All queries should extend this class to gain automatic observability features.

**Inheritance:**
```python
BaseQuery(BaseModel, IQuery)
```

**Fields:**

Same as `BaseCommand`:
- `request_id: UUID`
- `correlation_id: Optional[UUID]`
- `requested_by: Optional[str]`
- `requested_at: datetime`

**Configuration:**
- `frozen=True`: Queries are immutable after creation

**Example:**
```python
from python_cqrs_core import BaseQuery

class GetUserQuery(BaseQuery):
    user_id: int

# Usage
query = GetUserQuery(
    user_id=123,
    requested_by="john@example.com"
)

print(query.request_id)    # UUID('abc12345-...')
print(query.user_id)       # 123
```

### `PaginatedQuery`

Query with pagination support.

Extends `BaseQuery` with pagination fields and automatic offset calculation.

**Inheritance:**
```python
PaginatedQuery(BaseQuery)
```

**Fields:**

All `BaseQuery` fields, plus:

#### `page: int`
- **Type:** `int`
- **Default:** `1`
- **Constraints:** `>= 1` (1-indexed)
- **Description:** Page number
- **Usage:** Specify which page of results to retrieve

#### `page_size: int`
- **Type:** `int`
- **Default:** `10`
- **Constraints:** `1 <= page_size <= 100`
- **Description:** Items per page
- **Usage:** Control result set size (max 100 items)

**Properties:**

#### `offset: int`

Calculated offset for database queries.

**Formula:** `(page - 1) * page_size`

**Returns:**
- `int`: Offset value to use in database LIMIT/OFFSET queries

**Example:**
```python
from python_cqrs_core import PaginatedQuery

class ListUsersQuery(PaginatedQuery):
    status: str = "active"

# Page 1
query = ListUsersQuery(page=1, page_size=20)
print(query.offset)  # 0

# Page 3
query = ListUsersQuery(page=3, page_size=20)
print(query.offset)  # 40

# Use in database query
users = await db.query(User)\
    .offset(query.offset)\
    .limit(query.page_size)\
    .all()
```

## Type Hints

All interfaces and base classes support full generic type hints:

```python
from python_cqrs_core import IQueryHandler, BaseQuery
from typing import List

class ListUsersQuery(BaseQuery):
    status: str

class User:
    id: int
    name: str

# Handler with proper type hints
class ListUsersHandler(IQueryHandler[ListUsersQuery, List[User]]):
    async def handle(self, query: ListUsersQuery) -> List[User]:
        # Type checker knows:
        # - query is ListUsersQuery
        # - Must return List[User]
        return await self.repo.list(status=query.status)
```

## Immutability

All queries and commands are immutable (frozen) after creation:

```python
query = GetUserQuery(user_id=123)
query.user_id = 456  # ❌ Raises: FrozenInstanceError

# Must create new instance
new_query = GetUserQuery(user_id=456)  # ✅ OK
```

This ensures that queries/commands cannot be modified after creation, providing:
- Thread safety
- Predictable behavior
- Prevention of accidental mutations in handlers
