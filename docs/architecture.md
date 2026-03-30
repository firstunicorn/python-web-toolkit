# Architecture

## Layer hierarchy

```
Application layer (depends on Domain + Primitives)
├── gridflow-python-mediator
├── python-cqrs-dispatcher (depends on cqrs-core + mediator)
├── fastapi-config-patterns
├── fastapi-middleware-toolkit
├── python-structlog-config
├── python-outbox-core
├── sqlalchemy-async-session-factory
└── sqlalchemy-async-repositories

Domain layer (depends on Primitives only)
├── python-app-exceptions
├── python-infrastructure-exceptions
├── python-input-validation
├── python-cqrs-core
├── python-domain-events
├── python-dto-mappers
└── pydantic-response-models

Primitives layer (zero dependencies)
└── python-technical-primitives
```

## Import-linter contracts

Layer boundaries are enforced via `import-linter` in `pyproject.toml`:

- **Primitives** cannot import from domain or application
- **Domain** can import from primitives, cannot import from application
- **Application** can import from domain and primitives

## Inter-package dependencies

Only one cross-package dependency exists:

```
python-cqrs-dispatcher
├── python-cqrs-core (ICommand, IQuery interfaces)
└── gridflow-python-mediator  (Mediator dispatch engine)
```

All other packages are fully independent.

## Design patterns used

| Pattern | Package |
|---------|---------|
| Specification | `python-technical-primitives` |
| Repository + Strategy | `sqlalchemy-async-repositories` |
| Factory Method | `sqlalchemy-async-repositories` (pagination) |
| Mediator | `gridflow-python-mediator` |
| CQRS | `python-cqrs-core`, `python-cqrs-dispatcher` |
| Pipeline behaviors | `gridflow-python-mediator` |
| Transactional outbox | `python-outbox-core` |
| Strategy (formatters) | `python-outbox-core` |
| CloudEvents | `python-outbox-core` |
