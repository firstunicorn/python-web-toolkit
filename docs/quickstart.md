# Quickstart

## Installation

All packages are published to PyPI. Install only what you need:

```bash
pip install python-cqrs-core python-mediator python-cqrs-dispatcher
pip install sqlalchemy-async-session-factory sqlalchemy-async-repositories
pip install fastapi-config-patterns fastapi-middleware-toolkit
pip install python-structlog-config python-outbox-core
```

## Minimal working example

A FastAPI app with structured logging, typed settings, CORS, and a CQRS command:

```python
from fastapi import FastAPI
from python_structlog_config import configure_for_development
from fastapi_config_patterns import BaseFastAPISettings
from fastapi_middleware_toolkit import setup_cors_middleware
from python_cqrs_core import BaseCommand, ICommandHandler

configure_for_development("my-api")

class Settings(BaseFastAPISettings):
    app_name: str = "demo"

settings = Settings()
app = FastAPI(title=settings.app_name)
setup_cors_middleware(app, settings.allowed_origins)

class CreateUser(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUser, dict]):
    async def handle(self, cmd: CreateUser) -> dict:
        return {"name": cmd.name, "email": cmd.email}
```

## Layer architecture

Packages are organized in three layers (enforced by import-linter):

| Layer | Packages | Depends on |
|-------|----------|------------|
| **Primitives** | `python-technical-primitives` | nothing |
| **Domain** | exceptions, validation, CQRS core, events, DTOs, response models | primitives |
| **Application** | mediator, dispatcher, config, middleware, structlog, outbox, sessions, repositories | domain + primitives |
