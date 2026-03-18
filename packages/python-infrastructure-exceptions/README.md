# python-infrastructure-exceptions

Infrastructure layer exception classes for Python applications.

**Purpose:** Low-level infrastructure errors (database, network, external services).

**Separation:**
- **`python-infrastructure-exceptions`** = Infrastructure layer (DB, network, cache, queue)
- **`python-app-exceptions`** = Business/application layer (validation, business rules)

## Installation

```bash
pip install python-infrastructure-exceptions
```

## Usage

```python
from python_infrastructure_exceptions import (
    InfrastructureException,
    DatabaseError,
    ExternalServiceError,
    ConfigurationError,
    CacheError,
    MessageQueueError
)

# Database errors
raise DatabaseError("Connection pool exhausted", details="Max connections: 20")

# External service errors
raise ExternalServiceError("Stripe API timeout", service_name="stripe")

# Configuration errors
raise ConfigurationError("Missing DATABASE_URL environment variable")

# Cache errors
raise CacheError("Redis connection failed", details="Connection refused")

# Message queue errors
raise MessageQueueError("Kafka broker unavailable", details="broker.example.com:9092")
```

## Exception Hierarchy

```
InfrastructureException (base)
├── DatabaseError              # Database connection, query failures
├── ExternalServiceError       # Third-party API failures
├── ConfigurationError         # Missing/invalid configuration
├── CacheError                 # Redis, Memcached failures
└── MessageQueueError          # Kafka, RabbitMQ failures
```

## When to Use

| Exception Type | Use For | Example |
|----------------|---------|---------|
| **InfrastructureException** | Base class for custom infrastructure errors | Custom database adapter error |
| **DatabaseError** | Database connection, query, transaction failures | PostgreSQL connection pool exhausted |
| **ExternalServiceError** | Third-party API failures | Stripe API timeout, SendGrid error |
| **ConfigurationError** | Missing or invalid configuration | Missing `DATABASE_URL` env var |
| **CacheError** | Cache layer failures | Redis connection refused |
| **MessageQueueError** | Message broker failures | Kafka broker unavailable |

## Comparison with python-app-exceptions

| Layer | Library | Exceptions | Example |
|-------|---------|------------|---------|
| **Infrastructure** | `python-infrastructure-exceptions` | DatabaseError, ExternalServiceError | PostgreSQL timeout |
| **Business** | `python-app-exceptions` | ValidationError, BusinessRuleViolation | Invalid email format |

## Features

- ✅ Infrastructure-specific error types
- ✅ Detailed error context (service name, connection details)
- ✅ Framework-agnostic
- ✅ Zero dependencies
- ✅ Type-safe error handling

## License

MIT

