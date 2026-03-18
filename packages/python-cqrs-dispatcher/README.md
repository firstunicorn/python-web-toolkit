# Python CQRS Dispatcher

CQRS dispatcher that integrates `python-cqrs-core` with `python-mediator` for type-safe command/query dispatch.

## Installation

```bash
pip install python-cqrs-dispatcher
```

## Features

- **Type-Safe Dispatch**: Separate command/query dispatch methods
- **Handler Registry**: Track registered handlers
- **Pipeline Behaviors**: Built-in support via mediator
- **Bulk Registration**: Register multiple handlers at once
- **Auto-Discovery**: Auto-register handlers from modules

## Usage

### Basic Setup

```python
from python_cqrs_dispatcher import CQRSDispatcher
from python_cqrs_core import BaseCommand, ICommandHandler

class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    async def handle(self, command: CreateUserCommand) -> int:
        # Create user logic
        return user_id

# Setup dispatcher
dispatcher = CQRSDispatcher()
dispatcher.register_command_handler(
    CreateUserCommand,
    CreateUserHandler()
)

# Dispatch command
cmd = CreateUserCommand(name="John", email="john@example.com")
user_id = await dispatcher.send_command(cmd)
```

### With Queries

```python
from python_cqrs_core import BaseQuery, IQueryHandler

class GetUserQuery(BaseQuery):
    user_id: int

class GetUserHandler(IQueryHandler[GetUserQuery, User]):
    async def handle(self, query: GetUserQuery) -> User:
        return await db.get_user(query.user_id)

dispatcher.register_query_handler(GetUserQuery, GetUserHandler())

query = GetUserQuery(user_id=1)
user = await dispatcher.send_query(query)
```

### Bulk Registration

```python
from python_cqrs_dispatcher import register_handlers

handlers = [
    (CreateUserCommand, CreateUserHandler()),
    (UpdateUserCommand, UpdateUserHandler()),
    (GetUserQuery, GetUserHandler()),
    (ListUsersQuery, ListUsersHandler()),
]

register_handlers(dispatcher, handlers)
```

### Pipeline Behaviors

```python
from python_mediator import LoggingBehavior, TimingBehavior

# Add behaviors (execute before all handlers)
dispatcher.add_pipeline_behavior(LoggingBehavior().handle)
dispatcher.add_pipeline_behavior(TimingBehavior().handle)
```

### Auto-Registration

```python
from python_cqrs_dispatcher import auto_register_handlers
import my_app.handlers

# Auto-discover and register all handlers
auto_register_handlers(dispatcher, my_app.handlers)
```

## API Reference

### `CQRSDispatcher`

Type-safe CQRS dispatcher.

**Methods:**

#### `register_command_handler(command_type, handler)`

Register command handler.

**Parameters:**
- `command_type` (Type[ICommand]): Command class
- `handler` (ICommandHandler): Handler instance

#### `register_query_handler(query_type, handler)`

Register query handler.

**Parameters:**
- `query_type` (Type[IQuery]): Query class  
- `handler` (IQueryHandler): Handler instance

#### `async send_command(command) -> Any`

Dispatch command.

**Parameters:**
- `command` (ICommand): Command to dispatch

**Returns:**
- Command result

#### `async send_query(query) -> Any`

Dispatch query.

**Parameters:**
- `query` (IQuery): Query to dispatch

**Returns:**
- Query result

#### `add_pipeline_behavior(behavior)`

Add pipeline behavior.

**Parameters:**
- `behavior` (Callable): Behavior function

### Helper Functions

#### `register_handlers(dispatcher, handlers)`

Bulk register handlers.

**Parameters:**
- `dispatcher` (CQRSDispatcher): Dispatcher instance
- `handlers` (List[Tuple[Type, Any]]): Handler tuples

#### `auto_register_handlers(dispatcher, module)`

Auto-discover and register handlers.

**Parameters:**
- `dispatcher` (CQRSDispatcher): Dispatcher instance
- `module` (Module): Python module to scan

## Dependencies

- `python-cqrs-core>=0.1.0`
- `python-mediator>=0.1.0`

## License

MIT
