# Why Use BaseQuery/BaseCommand?

## Overview

While `BaseQuery` and `BaseCommand` extend Pydantic's `BaseModel`, they provide critical production-ready features that go beyond basic validation.

## Benefits

### 1. Zero-Effort Observability

Every query/command automatically gets tracing fields without manual declaration:

```python
# Plain Pydantic (NO observability)
class GetUserQuery(BaseModel):
    user_id: int
    # No way to track this request through logs

# With BaseQuery (FULL observability)
class GetUserQuery(BaseQuery):
    user_id: int
    # Automatically includes: request_id, correlation_id, requested_by, requested_at
```

### 2. Production Debugging

**Without BaseQuery:**
```python
# Handler logging
async def handle(self, query: GetUserQuery):
    logger.info("Processing GetUser")  # ❌ Which request? Who? When?
    return await self.repo.get(query.user_id)
```

**With BaseQuery:**
```python
# Handler logging
async def handle(self, query: GetUserQuery):
    logger.info(
        f"[{query.request_id}] Processing GetUser "
        f"for user_id={query.user_id} by {query.requested_by}"
    )
    result = await self.repo.get(query.user_id)
    
    duration = (datetime.now(timezone.utc) - query.requested_at).total_seconds()
    logger.info(f"[{query.request_id}] Retrieved user in {duration}s")
    return result
```

**Now in logs:**
```
[550e8400-...] Processing GetUser for user_id=123 by john@example.com
[550e8400-...] Retrieved user in 0.342s
```

### 3. Distributed Tracing

Link related operations across your system:

```python
# Initial command
save_cmd = SaveStateCommand(
    token="abc123",
    entity_id=1,
    requested_by="john@example.com"
)
await handler.handle(save_cmd)
# request_id: 550e8400-e29b-41d4-a716-446655440000

# Related command - link them!
finalize_cmd = FinalizeSessionCommand(
    token="abc123",
    correlation_id=save_cmd.request_id,  # ← Trace the relationship
    requested_by="john@example.com"
)
await handler.handle(finalize_cmd)

# Logs show the connection:
# [550e8400] SaveState for token=abc123
# [abc12345 | correlation: 550e8400] FinalizeSession for token=abc123
```

### 4. Audit Trail for Compliance

Track who did what and when:

```python
cmd = CreateInviteCommand(
    email="user@example.com",
    expires_in_days=7,
    requested_by="admin@example.com"  # ← Audit trail
)

# Later, in your database/logs:
# "Invite created by admin@example.com at 2026-02-26 10:30:45 [request: 550e8400]"
```

### 5. Built-in Immutability

Prevent accidental mutations:

```python
query = GetUserQuery(user_id=123)
query.user_id = 456  # ❌ FrozenInstanceError
# Ensures queries/commands can't be tampered with after creation
```

### 6. Performance Monitoring

Track execution times automatically:

```python
async def handle(self, query: GetUserQuery):
    start = query.requested_at
    result = await self.repo.get(query.user_id)
    duration = (datetime.now(timezone.utc) - start).total_seconds()
    
    # Send to monitoring system
    metrics.record_query_duration(
        query_type="GetUser",
        duration=duration,
        request_id=str(query.request_id)
    )
    return result
```

## When to Use Plain BaseModel vs BaseQuery/BaseCommand

| Use Case | Use Plain BaseModel | Use BaseQuery/BaseCommand |
|----------|---------------------|---------------------------|
| **API Request/Response DTOs** | ✅ Yes | ❌ No (too many fields) |
| **Internal Data Transfer** | ✅ Yes | ❌ No (overhead) |
| **CQRS Commands** | ❌ No | ✅ **YES** (tracing needed) |
| **CQRS Queries** | ❌ No | ✅ **YES** (tracing needed) |
| **Domain Events** | ✅ Maybe | ✅ Maybe (if tracing needed) |
| **Configuration Objects** | ✅ Yes | ❌ No (static data) |

## Real-World Scenario

Imagine debugging a production issue:

```
❌ Without BaseQuery:
User reports: "My state save failed 10 minutes ago"
You search logs: 
  "Error: Token not found"  
  "Error: Token not found"  
  "Error: Token not found"
→ Which error is theirs? No way to know. No timestamp. No user ID.

✅ With BaseQuery:
User reports: "My state save failed 10 minutes ago" 
You search logs for their email in requested_by:
  "[550e8400] Error: Token not found | token=abc123 | user=john@example.com | at=2026-02-26 10:20:45"
→ Found it immediately! Can now trace the full request flow.
```

## The Bottom Line

**BaseQuery/BaseCommand = BaseModel + Production-Ready Observability**

- Same Pydantic validation
- Same performance
- **+ Automatic tracing**
- **+ Audit trail**
- **+ Immutability**
- **+ Debug-friendly**

**Cost:** 4 optional fields (~100 bytes per instance)  
**Benefit:** Complete production observability and audit trail

**Use BaseQuery/BaseCommand for all CQRS operations. Use plain BaseModel for everything else.**

## Design Patterns

### CQRS Pattern

Separates read and write operations:
- **Commands**: Modify state (CREATE, UPDATE, DELETE)
- **Queries**: Read state (GET, LIST)

This separation provides:
- Independent scaling of reads and writes
- Optimized data models for each operation type
- Clear intent in your codebase

### Handler Pattern

Each command/query has a dedicated handler:
- **Single responsibility**: Each handler does one thing
- **Easy to test**: Isolated business logic
- **Composable with middleware**: Add logging, validation, authorization

**Example:**
```python
# Command and its dedicated handler
class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, int]):
    async def handle(self, command: CreateUserCommand) -> int:
        # Single responsibility: create a user
        return await self.user_repository.create(command)

# Query and its dedicated handler
class GetUserQuery(BaseQuery):
    user_id: int

class GetUserHandler(IQueryHandler[GetUserQuery, User]):
    async def handle(self, query: GetUserQuery) -> User:
        # Single responsibility: fetch a user
        return await self.user_repository.get(query.user_id)
```
