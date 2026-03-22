# python-cqrs-dispatcher

CQRS dispatcher integrating `python-cqrs-core` interfaces with `python-mediator`.

## Installation

```bash
pip install python-cqrs-dispatcher
```

## Public API

| Symbol | Purpose |
|--------|---------|
| `CQRSDispatcher` | Type-safe CQRS dispatch (commands + queries) |
| `register_handlers(dispatcher, handlers)` | Bulk handler registration |
| `auto_register_handlers(dispatcher, module)` | Auto-discover handlers from module |

## Usage

```python
from python_cqrs_dispatcher import CQRSDispatcher

dispatcher = CQRSDispatcher()
dispatcher.register_command_handler(CreateUser, CreateUserHandler())
dispatcher.register_query_handler(GetUser, GetUserHandler())

result = await dispatcher.send_command(CreateUser(name="Alice"))
user = await dispatcher.send_query(GetUser(user_id=1))
```

## Bulk registration

```python
from python_cqrs_dispatcher import register_handlers

register_handlers(dispatcher, [
    (CreateUser, CreateUserHandler()),
    (GetUser, GetUserHandler()),
])
```
