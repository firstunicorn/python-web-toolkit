# Usage Examples

Complete examples showing how to use all 16 Python Web Toolkit libraries.

## Quick Start

New to these libraries? Start here:

**[Quick Start Guide](QUICK_START.md)** - 5 essential examples covering the most common workflows

## All Examples by Layer & Use Case

### Domain & Application Layer

**Building APIs**
- [Example 1: FastAPI Application](domain/building-apis.md#example-1-fastapi-application) - Basic API with repositories, validation, and error handling
- [Example 7: Complete REST API](domain/building-apis.md#example-7-complete-rest-api) - REST API with response models and pagination

**Data Patterns**
- [Example 2: Domain Model with Specification Pattern](domain/data-patterns.md#example-2-domain-model-with-specification-pattern) - Composable business rules
- [Example 3: Data Sanitization Pipeline](domain/data-patterns.md#example-3-data-sanitization-pipeline) - PostgreSQL-safe data processing

**Utilities**
- [Example 4: String Utilities](domain/utilities.md#example-4-string-utilities) - Text operations and transformations
- [Example 5: DateTime Operations](domain/utilities.md#example-5-datetime-operations) - Timezone-aware date/time handling

**Error Handling**
- [Example 6: Exception Handling Hierarchy](domain/error-handling.md#example-6-exception-handling-hierarchy) - Structured exception management

### Infrastructure & Middleware

**Building APIs**
- [Example 8: Complete FastAPI Setup with Middleware](infrastructure/building-apis.md#example-8-complete-fastapi-setup-with-middleware) - CORS, error handlers, lifespan, health checks

**Operations**
- [Example 9: Structured Logging Configuration](infrastructure/operations.md#example-9-structured-logging-configuration) - Development, production, and testing logging presets

**Data Patterns**
- [Example 10: SQLAlchemy Async Session Management](infrastructure/data-patterns.md#example-10-sqlalchemy-async-session-management) - Engine, sessions, FastAPI dependencies
- [Example 13: DTO Auto-Mapping](infrastructure/data-patterns.md#example-13-dto-auto-mapping) - Automatic object-to-DTO transformations

**Application Patterns**
- [Example 11: CQRS Pattern with Commands & Queries](infrastructure/application-patterns.md#example-11-cqrs-pattern-with-commands--queries) - Separated read/write operations
- [Example 12: Mediator with Pipeline Behaviors](infrastructure/application-patterns.md#example-12-mediator-with-pipeline-behaviors) - Request pipeline with logging, timing, validation

**Messaging Patterns**
- [Example 14: Transactional Outbox Pattern](infrastructure/messaging-patterns.md#example-14-transactional-outbox-pattern) - Reliable event publishing

**Complete Integration**
- [Example 15: Complete Backend Application](infrastructure/complete-backend-application.md#example-15-complete-backend-application) - Full backend integrating all 16 libraries

## Installation

### Domain & Application Layer (6 libraries)

```bash
pip install python-app-exceptions>=0.1.0
pip install pydantic-response-models>=0.1.0
pip install sqlalchemy-async-repositories>=0.1.0
pip install python-technical-primitives>=0.1.0
pip install postgres-data-sanitizers>=0.1.0
pip install python-input-validation>=0.1.0
```

### Infrastructure & Middleware (10 libraries)

```bash
pip install fastapi-middleware-toolkit>=0.1.0
pip install fastapi-config-patterns>=0.1.0
pip install sqlalchemy-async-session-factory>=0.1.0
pip install python-structlog-config>=0.1.0
pip install python-infrastructure-exceptions>=0.1.0
pip install python-dto-mappers>=0.1.0
pip install python-cqrs-core>=0.1.0
pip install gridflow-python-mediator>=0.1.0
pip install python-cqrs-dispatcher>=0.1.0
pip install python-outbox-core>=0.1.0
```

## About the Libraries

All libraries are framework-agnostic (except FastAPI-specific ones) and work with FastAPI, Flask, Django, or any Python web framework. They follow SOLID principles, maintain strict file size limits (< 120 lines), and are production-tested from the GridFlow project.
