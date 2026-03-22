# sqlalchemy-async-repositories

Generic async repository pattern for SQLAlchemy with hybrid pagination (native + FastCRUD).

## Installation

```bash
pip install sqlalchemy-async-repositories

# with FastCRUD support:
pip install sqlalchemy-async-repositories[fastcrud]
```

## Public API

| Class | Purpose |
|-------|---------|
| `IRepository` | Abstract repository interface (CRUD) |
| `BaseRepository` | Orchestrates use-case handlers |
| `FilterSpec` / `SortSpec` | Query specifications |
| `PaginatedResult` | Typed pagination wrapper |

## Architecture docs

```{include} ../../packages/sqlalchemy-async-repositories/ARCHITECTURE.md
```

```{include} ../../packages/sqlalchemy-async-repositories/HYBRID_IMPLEMENTATION_SUMMARY.md
```

```{include} ../../packages/sqlalchemy-async-repositories/REFACTORING_SUMMARY_FACTORY_PATTERN.md
```
