# python-outbox-core

Core abstractions for the transactional outbox pattern (Kafka, FastStream, RabbitMQ).

## Installation

```bash
pip install python-outbox-core
```

## Public API

| Class | Purpose |
|-------|---------|
| `IOutboxEvent` | Abstract event base (Pydantic) |
| `IOutboxRepository` | Persistence interface |
| `IEventPublisher` | Broker publishing interface |
| `OutboxPublisherBase` | Reusable worker logic |
| `OutboxConfig` | Worker configuration |
| `OutboxErrorHandler` | Per-event error handling |
| `OutboxMetrics` | Structured logging metrics |
| `CloudEventsFormatter` | CloudEvents 1.0 formatting |
| `OutboxHealthCheck` | Health check interface |

## Quick reference

```{include} ../../packages/python-outbox-core/QUICKREF.md
```

## Detailed guides

```{include} ../../packages/python-outbox-core/detailed-docs/API_REFERENCE.md
```

```{include} ../../packages/python-outbox-core/detailed-docs/IMPLEMENTATION_GUIDE.md
```

## FAQ

```{include} ../../packages/python-outbox-core/detailed-docs/faq/OUTBOX_VS_TASK_QUEUES.md
```

```{include} ../../packages/python-outbox-core/detailed-docs/faq/SERIALIZATION_NOTES.md
```
