# Outbox Core - Extensibility Examples

This directory contains **minimal examples** demonstrating extensibility patterns.

## ⚠️ Important

These are **educational examples**, NOT production-ready code.

For production use:
- **Kong Integration**: Use `python-kong-integration` package
- **Kafka Publishing**: Use `python-outbox-faststream` package

## Extensibility Pattern

1. **Core defines protocol**: `IEventFormatter`
2. **Core provides base**: `CloudEventsFormatter`
3. **Examples show pattern**: `KongSimpleFormatter`
4. **Production packages extend**: `python-kong-integration`
5. **Your project customizes**: `GridFlowKongFormatter`

## Links

- [python-outbox-core README](../../README.md)
- [python-kong-integration](../../../python-kong-integration/)
- [python-outbox-faststream](../../../python-outbox-faststream/)
