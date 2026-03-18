# Python CQRS Core Documentation

Welcome to the Python CQRS Core documentation!

## Quick Links

### Getting Started
- [Usage Guide](docs/usage-guide.md) - Commands, queries, and examples
- [Why Use BaseQuery/BaseCommand?](docs/why-use-base-classes.md) - Benefits and use cases

### Integration Guides
- [Observability Integration](docs/observability.md) - OpenTelemetry, Sentry, Prometheus

### Reference
- [API Reference](docs/api-reference.md) - Complete API documentation

## What is Python CQRS Core?

CQRS (Command Query Responsibility Segregation) interfaces and base classes with built-in tracing and audit support for Python applications.

## Installation

```bash
pip install python-cqrs-core
```

## Key Features

- **Command/Query Separation**: Type-safe CQRS pattern implementation
- **Built-in Observability**: Automatic request IDs, correlation IDs, audit fields
- **Immutability**: Frozen commands/queries prevent tampering
- **Pagination**: Built-in pagination support for queries
- **Type Safety**: Full generic type support with type hints
- **Integration-Ready**: Works seamlessly with OpenTelemetry, Sentry, Prometheus

## Quick Example

```python
from python_cqrs_core import BaseCommand, ICommandHandler

class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    async def handle(self, command: CreateUserCommand) -> int:
        # Automatic tracing fields available:
        logger.info(
            f"[{command.request_id}] Creating user {command.email} "
            f"requested by {command.requested_by}"
        )

        user_id = await self.user_repository.create(
            name=command.name,
            email=command.email
        )

        return user_id
```

## Documentation Structure

### [Usage Guide](docs/usage-guide.md)

Practical examples and best practices:
- Commands and command handlers
- Queries and query handlers
- Paginated queries
- Tracing fields (request_id, correlation_id, requested_by, requested_at)
- Complete examples with logging and monitoring

### [Why Use BaseQuery/BaseCommand?](docs/why-use-base-classes.md)

Learn about the benefits of using `BaseQuery` and `BaseCommand` over plain Pydantic models:
- Zero-effort observability
- Production debugging
- Distributed tracing
- Audit trail for compliance
- Performance monitoring
- When to use vs plain BaseModel

### [Observability Integration](docs/observability.md)

Comprehensive guide to integrating with modern observability tools:
- OpenTelemetry integration patterns
- Sentry error tracking with business context
- Prometheus metrics with domain fields
- Audit trail for compliance (SOC 2, HIPAA, PCI DSS)
- Real-world examples and best practices

### [API Reference](docs/api-reference.md)

Complete API documentation:
- Interfaces: `ICommand`, `ICommandHandler`, `IQuery`, `IQueryHandler`
- Base Classes: `BaseCommand`, `BaseQuery`, `PaginatedQuery`
- Type hints and generics
- Immutability guarantees

## Dependencies

- `pydantic>=2.0.0`

## License

MIT
