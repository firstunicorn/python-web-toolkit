# python-cqrs-core

CQRS interfaces and base classes with built-in tracing and audit fields.

## Installation

```bash
pip install python-cqrs-core
```

## Public API

| Class | Purpose |
|-------|---------|
| `ICommand` | Write operation interface |
| `ICommandHandler` | Command handler with `handle()` |
| `IQuery` | Read operation interface |
| `IQueryHandler` | Query handler with `handle()` |
| `BaseCommand` | Pydantic command with `trace_id`, `user_id` |
| `BaseQuery` | Pydantic query with tracing fields |
| `PaginatedQuery` | Query with `page`, `page_size`, `offset` |

## Guides

```{include} ../../packages/python-cqrs-core/docs/usage-guide.md
```

```{include} ../../packages/python-cqrs-core/docs/api-reference.md
```

```{include} ../../packages/python-cqrs-core/docs/observability.md
```

```{include} ../../packages/python-cqrs-core/docs/why-use-base-classes.md
```
