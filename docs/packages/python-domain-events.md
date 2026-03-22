# python-domain-events

Base classes for internal (in-process) domain events with tracing.

## Installation

```bash
pip install python-domain-events
```

## Public API

| Class | Purpose |
|-------|---------|
| `BaseDomainEvent` | Pydantic base for domain events |
| `IDomainEventHandler[TEvent]` | Handler interface with `handle(event)` |
| `InProcessEventDispatcher` | Dispatches events to registered handlers |

## Usage

```python
from python_domain_events import BaseDomainEvent, IDomainEventHandler
from python_domain_events import InProcessEventDispatcher

class UserCreated(BaseDomainEvent):
    event_type: str = "user_created"
    user_id: int

class NotifyHandler(IDomainEventHandler[UserCreated]):
    def handle(self, event: UserCreated) -> None:
        print(f"User {event.user_id} created")

dispatcher = InProcessEventDispatcher()
dispatcher.register(UserCreated, NotifyHandler())
dispatcher.dispatch(UserCreated(event_type="user_created", user_id=1))
```
