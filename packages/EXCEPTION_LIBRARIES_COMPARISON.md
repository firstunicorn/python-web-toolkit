# Exception Libraries Comparison

## Two Separate Libraries for Two Layers

| Library | Layer | Purpose | When to Use |
|---------|-------|---------|-------------|
| **`python-infrastructure-exceptions`** | Infrastructure | Low-level technical failures | Database, network, cache, queues, external APIs |
| **`python-app-exceptions`** | Business/Application | High-level business failures | Validation, business rules, domain logic |

---

## Clear Separation of Concerns

```
┌─────────────────────────────────────────────────────────┐
│                    Application Code                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────┐       │
│  │  Business/Application Layer                   │       │
│  │  (Domain logic, use cases, validation)       │       │
│  │                                               │       │
│  │  Uses: python-app-exceptions                 │       │
│  │  - ValidationError                            │       │
│  │  - BusinessRuleViolation                      │       │
│  │  - ResourceNotFoundError                      │       │
│  └──────────────────────────────────────────────┘       │
│                        ↓                                  │
│  ┌──────────────────────────────────────────────┐       │
│  │  Infrastructure Layer                         │       │
│  │  (Database, cache, message queue, APIs)      │       │
│  │                                               │       │
│  │  Uses: python-infrastructure-exceptions      │       │
│  │  - DatabaseError                              │       │
│  │  - ExternalServiceError                       │       │
│  │  - CacheError                                 │       │
│  │  - MessageQueueError                          │       │
│  └──────────────────────────────────────────────┘       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## `python-infrastructure-exceptions`

**Purpose:** Low-level infrastructure failures

### Exception Types:
- `InfrastructureException` (base)
- `DatabaseError` - Database connection/query failures
- `ExternalServiceError` - Third-party API failures
- `ConfigurationError` - Missing/invalid configuration
- `CacheError` - Redis, Memcached failures
- `MessageQueueError` - Kafka, RabbitMQ failures

### Examples:
```python
from python_infrastructure_exceptions import (
    DatabaseError,
    ExternalServiceError,
    CacheError
)

# Database connection failure
raise DatabaseError(
    "Connection pool exhausted",
    details="Max connections: 20"
)

# External API timeout
raise ExternalServiceError(
    "Stripe API timeout",
    service_name="stripe",
    status_code=504
)

# Cache unavailable
raise CacheError(
    "Redis connection failed",
    cache_backend="redis",
    details="Connection refused to localhost:6379"
)
```

### When to Use:
- ✅ Database connection pool exhausted
- ✅ PostgreSQL query timeout
- ✅ Redis connection refused
- ✅ Kafka broker unavailable
- ✅ External API (Stripe, SendGrid) timeout
- ✅ Missing `DATABASE_URL` environment variable

---

## `python-app-exceptions`

**Purpose:** High-level business/application failures

### Exception Types:
- `BaseApplicationException` (base)
- `ValidationError` - Input validation failures
- `BusinessRuleViolation` - Domain rule violations
- `ResourceNotFoundError` - Entity not found
- `ConflictError` - Resource conflict (e.g., duplicate email)

### Examples:
```python
from python_app_exceptions import (
    ValidationError,
    BusinessRuleViolation,
    ResourceNotFoundError
)

# Invalid user input
raise ValidationError(
    "Invalid email format",
    field="email",
    details="Must be valid RFC 5322 email"
)

# Business rule violation
raise BusinessRuleViolation(
    "Cannot delete active subscription",
    details="User has active premium subscription"
)

# Resource not found
raise ResourceNotFoundError(
    "User not found",
    resource_type="User",
    resource_id=123
)
```

### When to Use:
- ✅ Invalid email format
- ✅ Password too short
- ✅ User not found
- ✅ Invite already used
- ✅ Token expired
- ✅ Cannot delete active subscription (business rule)

---

## Decision Tree: Which Exception to Use?

```
Is it a technical/infrastructure failure?
├─ YES → python-infrastructure-exceptions
│         └─ Examples: DB timeout, API failure, cache down
│
└─ NO → Is it a business/validation failure?
          └─ YES → python-app-exceptions
                   └─ Examples: Invalid email, token expired, user not found
```

---

## Code Examples: Error Handling

### Infrastructure Layer (Repository)
```python
from python_infrastructure_exceptions import DatabaseError
from python_app_exceptions import ResourceNotFoundError

class UserRepository:
    async def get_by_id(self, user_id: int) -> User:
        try:
            result = await self.db.execute(...)
        except asyncpg.exceptions.ConnectionDoesNotExistError as e:
            # Infrastructure failure
            raise DatabaseError(
                "Database connection lost",
                details=str(e)
            )

        if not result:
            # Business failure (not found)
            raise ResourceNotFoundError(
                "User not found",
                resource_type="User",
                resource_id=user_id
            )

        return result
```

### Application Layer (Use Case)
```python
from python_app_exceptions import ValidationError, BusinessRuleViolation

class CreateInviteCommandHandler:
    async def handle(self, command: CreateInviteCommand):
        # Validate input (business layer)
        if not is_valid_email(command.email):
            raise ValidationError(
                "Invalid email format",
                field="email"
            )

        # Check business rule (business layer)
        if await self.repo.count_active_invites() > MAX_INVITES:
            raise BusinessRuleViolation(
                "Maximum invite limit reached",
                details=f"Max: {MAX_INVITES}"
            )

        # Create invite
        # (repository may raise DatabaseError if DB is down)
        return await self.repo.create(command)
```

### Presentation Layer (API)
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from python_infrastructure_exceptions import InfrastructureException
from python_app_exceptions import BaseApplicationException

app = FastAPI()

@app.exception_handler(BaseApplicationException)
async def app_exception_handler(request: Request, exc: BaseApplicationException):
    """Handle business/application exceptions → 400 Bad Request"""
    return JSONResponse(
        status_code=400,
        content={"error": exc.message, "details": exc.details}
    )

@app.exception_handler(InfrastructureException)
async def infra_exception_handler(request: Request, exc: InfrastructureException):
    """Handle infrastructure exceptions → 500 Internal Server Error"""
    logger.error(f"Infrastructure failure: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}  # Don't expose details!
    )
```

---

## Summary

| Concern | python-infrastructure-exceptions | python-app-exceptions |
|---------|----------------------------------|----------------------|
| **Layer** | Infrastructure | Business/Application |
| **Purpose** | Technical failures | Business failures |
| **Examples** | DB timeout, API failure, cache down | Invalid email, user not found, business rule violation |
| **HTTP Status** | 500 (Internal Server Error) | 400 (Bad Request), 404 (Not Found), 409 (Conflict) |
| **Expose Details?** | ❌ NO (security risk) | ✅ YES (help users fix input) |
| **Logging** | ✅ Always log | ⚠️ Optional (user errors) |

---

## Migration Guide

### Before (Mixed Exceptions)
```python
# ❌ Everything inherits from a single base
class GridFlowException(Exception):
    pass

class DatabaseError(GridFlowException):  # Infrastructure
    pass

class ValidationError(GridFlowException):  # Business
    pass
```

### After (Separated by Layer)
```python
# ✅ Infrastructure layer
from python_infrastructure_exceptions import DatabaseError

# ✅ Business layer
from python_app_exceptions import ValidationError
```

---

**Result:** Clear separation of concerns, better error handling, and improved security! 🎉

