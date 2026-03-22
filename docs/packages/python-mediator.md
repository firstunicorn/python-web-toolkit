# python-mediator

Generic mediator pattern with pipeline behaviors for cross-cutting concerns.

## Installation

```bash
pip install python-mediator
```

## Public API

| Class | Purpose |
|-------|---------|
| `Mediator` | Request/response dispatcher |
| `PipelineBehavior` | Protocol for pipeline behaviors |
| `LoggingBehavior` | Logs request handling |
| `TimingBehavior` | Times request execution |
| `ValidationBehavior` | Validates Pydantic models before dispatch |

## Usage

```python
from python_mediator import Mediator
from python_mediator.behaviors import LoggingBehavior, ValidationBehavior

mediator = Mediator()
mediator.add_pipeline_behavior(LoggingBehavior())
mediator.add_pipeline_behavior(ValidationBehavior())
mediator.register_handler(MyRequest, MyHandler())

result = await mediator.send(MyRequest(data="test"))
```

## Pipeline behavior protocol

```python
class MyBehavior:
    async def handle(self, request, next):
        # pre-processing
        result = await next(request)
        # post-processing
        return result
```
