# gridflow-python-mediator

Generic mediator pattern implementation with zero dependencies and pipeline behavior support.

**Extracted from:** GridFlow `backend/src/apps/token_generator/application/common/mediator/`

## Installation

```bash
# Core (zero dependencies)
pip install gridflow-python-mediator

# With logging support
pip install gridflow-python-mediator[logging]
```

## Features

- **Zero Dependencies**: Pure Python implementation
- **Pipeline Behaviors**: Logging, timing, validation
- **Type-Safe**: Full generic type support
- **Async/Sync**: Supports both async and sync handlers

## Usage

### Basic Mediator

```python
from gridflow_python_mediator import Mediator

# Define request and handler
class GetUserRequest:
    def __init__(self, user_id: int):
        self.user_id = user_id

class GetUserHandler:
    async def handle(self, request: GetUserRequest):
        # Fetch user logic
        return {"id": request.user_id, "name": "John"}

# Setup mediator
mediator = Mediator()
mediator.register_handler(GetUserRequest, GetUserHandler())

# Send request
request = GetUserRequest(user_id=1)
result = await mediator.send(request)
```

### With CQRS

```python
from python_cqrs_core import BaseCommand, ICommandHandler
from gridflow_python_mediator import Mediator

class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    async def handle(self, command: CreateUserCommand) -> int:
        # Create user
        return user_id

mediator = Mediator()
mediator.register_handler(CreateUserCommand, CreateUserHandler())

cmd = CreateUserCommand(name="John", email="john@example.com")
user_id = await mediator.send(cmd)
```

### Pipeline Behaviors

```python
from gridflow_python_mediator import (
    Mediator,
    LoggingBehavior,
    TimingBehavior,
    ValidationBehavior
)

mediator = Mediator()

# Add behaviors (executed in order)
mediator.add_pipeline_behavior(LoggingBehavior().handle)
mediator.add_pipeline_behavior(TimingBehavior().handle)
mediator.add_pipeline_behavior(ValidationBehavior().handle)

# Behaviors run before handler
result = await mediator.send(request)
```

### Custom Behavior

```python
async def auth_behavior(request, handler):
    """Check authentication before handler."""
    if not request.user_id:
        raise ValueError("Unauthorized")
    return None  # Continue to handler

mediator.add_pipeline_behavior(auth_behavior)
```

## API Reference

### `Mediator`

Generic request/response dispatcher.

**Methods:**

#### `register_handler(request_type, handler)`

Register handler for request type.

**Parameters:**
- `request_type` (Type): Request class
- `handler` (Any): Handler instance with `handle()` method

#### `async send(request) -> TResult`

Dispatch request to handler.

**Parameters:**
- `request` (TRequest): Request to send

**Returns:**
- Result from handler

#### `add_pipeline_behavior(behavior)`

Add pipeline behavior.

**Parameters:**
- `behavior` (Callable): Async function(request, handler) -> Optional[result]

### Built-in Behaviors

#### `LoggingBehavior`

Logs request type before/after handler.

**Requires:** `structlog>=23.0.0`

#### `TimingBehavior`

Measures and logs execution duration.

**Requires:** `structlog>=23.0.0`

#### `ValidationBehavior`

Validates Pydantic models before handler.

## Design Patterns

### Mediator Pattern

Decouples senders from receivers:
- Single point of dispatch
- Handler registration
- Pipeline behaviors

### Pipeline Pattern

Behaviors execute in order:
1. Logging
2. Timing
3. Validation
4. Handler

## Dependencies

- **Core**: None (zero dependencies!)
- **Optional**: `structlog>=23.0.0` (for logging behaviors)

## License

MIT
