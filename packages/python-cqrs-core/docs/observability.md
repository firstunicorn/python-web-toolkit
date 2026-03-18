# Observability Integration

## Overview

`BaseQuery` and `BaseCommand` are designed to work seamlessly with modern observability tools like **OpenTelemetry**, **Sentry**, and **Prometheus**. They provide the crucial **business context layer** that complements infrastructure tracing.

## Key Insight: Complementary, Not Redundant

### Infrastructure Tracing vs Domain Tracing

| Aspect | OpenTelemetry/Sentry/Prometheus | BaseQuery/BaseCommand |
|--------|--------------------------------|------------------------|
| **Purpose** | Technical/infrastructure tracing | Business/domain context |
| **What it tracks** | HTTP calls, DB queries, spans, metrics | Who, what, when at domain level |
| **IDs** | Opaque trace IDs (`abc123def456...`) | Business IDs (`request_id`, `order_id`) |
| **Searchability** | By trace ID, span name | By user, email, business entity |
| **Compliance** | Must add explicit audit events | Built-in audit trail |
| **Best for** | "What's slow?", "Where did it fail?" | "Who did this?", "What business operation?" |

**Bottom line:** Infrastructure tools show **HOW** your system works. Your BaseQuery/BaseCommand fields provide **WHO and WHAT** at the business level.

## Integration Pattern: The Bridge

Your `BaseQuery`/`BaseCommand` fields become the **attributes** you attach to OpenTelemetry spans and Sentry events.

```
Domain Layer (Your Code)
  ↓ BaseQuery/BaseCommand with business fields
  ↓
Handler Layer  
  ↓ Attach business fields to OTel span attributes
  ↓
Infrastructure Layer (OpenTelemetry)
  ↓ Technical tracing (HTTP, DB, cache, etc.)
  ↓
Observability Tools (Sentry/Prometheus/Jaeger)
  ↓ Unified view: Business context + Technical trace
```

## OpenTelemetry Integration

### Setup

```bash
pip install opentelemetry-api opentelemetry-sdk
```

### Pattern 1: Attach Command/Query Context to Spans

Create a helper to bridge your domain fields to OpenTelemetry:

```python
from opentelemetry import trace
from python_cqrs_core import BaseCommand, BaseQuery
from typing import Union

def attach_cqrs_context(
    span: trace.Span, 
    cqrs_object: Union[BaseCommand, BaseQuery]
):
    """Attach BaseCommand/BaseQuery fields to OpenTelemetry span."""
    span.set_attribute("business.request_id", str(cqrs_object.request_id))
    
    if cqrs_object.correlation_id:
        span.set_attribute("business.correlation_id", str(cqrs_object.correlation_id))
    
    if cqrs_object.requested_by:
        span.set_attribute("requested_by", cqrs_object.requested_by)
    
    span.set_attribute("requested_at", cqrs_object.requested_at.isoformat())
    
    # Determine if it's a command or query
    span.set_attribute(
        "cqrs.type", 
        "command" if isinstance(cqrs_object, BaseCommand) else "query"
    )
    span.set_attribute("cqrs.name", type(cqrs_object).__name__)
```

### Pattern 2: Use in Your Handlers

```python
from opentelemetry import trace

class CreateInviteCommandHandler:
    def __init__(self, repository):
        self.repository = repository
        self.tracer = trace.get_tracer("cqrs.write", "1.0.0")
    
    async def handle(self, command: CreateInviteCommand):
        with self.tracer.start_as_current_span("CreateInvite") as span:
            # Attach your domain context
            attach_cqrs_context(span, command)
            
            # Add business-specific attributes
            span.set_attribute("invite.email", command.email)
            span.set_attribute("invite.expires_in_days", command.expires_in_days)
            
            # Execute business logic
            result = await self.repository.create(command)
            
            # Add result attributes
            span.set_attribute("result.invite_id", result.id)
            span.set_attribute("result.token", result.token)
            
            return result
```

### Pattern 3: Propagate Correlation IDs via Baggage

Use OpenTelemetry baggage to propagate your correlation IDs downstream:

```python
from opentelemetry import baggage, context

async def handle(self, command: CreateInviteCommand):
    # Set correlation_id in baggage for downstream services
    correlation_id = str(command.correlation_id or command.request_id)
    
    ctx = baggage.set_baggage("correlation.id", correlation_id)
    
    with self.tracer.start_as_current_span("CreateInvite", context=ctx) as span:
        attach_cqrs_context(span, command)
        # All downstream services get correlation.id automatically!
        result = await self.repository.create(command)
        return result
```

### Pattern 4: Separate Command and Query Tracers (Best Practice 2026)

Create separate tracers for read and write paths:

```python
# In your application setup
write_tracer = trace.get_tracer("cqrs.write", "1.0.0")
read_tracer = trace.get_tracer("cqrs.read", "1.0.0")

# Command handlers use write tracer
class CreateInviteHandler:
    tracer = write_tracer

# Query handlers use read tracer  
class GetInviteHandler:
    tracer = read_tracer
```

This enables independent monitoring of write-side throughput vs read-side latency.

## Sentry Integration

### Setup

```bash
pip install sentry-sdk opentelemetry-sdk
```

### Pattern 1: Automatic Trace Context Correlation

Initialize OpenTelemetry first, then Sentry with OpenTelemetry integration:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
import sentry_sdk
from sentry_sdk.integrations.opentelemetry import OpenTelemetryIntegration

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())

# Initialize Sentry with OTel integration
sentry_sdk.init(
    dsn="your-dsn",
    integrations=[OpenTelemetryIntegration()],
    traces_sample_rate=1.0,
)
```

Now Sentry automatically picks up OpenTelemetry trace context, and your `BaseCommand`/`BaseQuery` fields flow through!

### Pattern 2: Attach Context to Sentry Scope

```python
import sentry_sdk

async def handle(self, command: CreateInviteCommand):
    with sentry_sdk.configure_scope() as scope:
        # Add your business context
        scope.set_tag("business.request_id", str(command.request_id))
        scope.set_tag("requested_by", command.requested_by)
        scope.set_context("command", {
            "type": type(command).__name__,
            "request_id": str(command.request_id),
            "correlation_id": str(command.correlation_id) if command.correlation_id else None,
            "requested_by": command.requested_by,
            "requested_at": command.requested_at.isoformat(),
        })
        
        # Execute command
        result = await self.repository.create(command)
        return result
```

### Pattern 3: Search Sentry by Business Context

When errors occur, search Sentry by your domain fields:

```
# User reports: "My invite creation failed"
# User email: john@example.com

Search Sentry:
  requested_by:"john@example.com" AND type:"CreateInviteCommand"

Result:
  Error: DatabaseError
  ↳ business.request_id: 550e8400-e29b-41d4-a716-446655440000
  ↳ requested_by: john@example.com
  ↳ command.type: CreateInviteCommand
  ↳ OTel Trace ID: abc123def456...
  
Click trace ID → See full distributed trace!
```

## Prometheus Integration

### Pattern: Use request_id for Request Duration Metrics

```python
from prometheus_client import Histogram
from datetime import datetime, timezone

# Define metric
command_duration = Histogram(
    'cqrs_command_duration_seconds',
    'Command execution duration',
    ['command_type', 'requested_by', 'status']
)

async def handle(self, command: CreateInviteCommand):
    start = command.requested_at
    status = "success"
    
    try:
        result = await self.repository.create(command)
        return result
    except Exception as e:
        status = "error"
        raise
    finally:
        duration = (datetime.now(timezone.utc) - start).total_seconds()
        
        # Record metric with business context
        command_duration.labels(
            command_type=type(command).__name__,
            requested_by=command.requested_by or "anonymous",
            status=status
        ).observe(duration)
```

### Pattern: Counter by User

```python
from prometheus_client import Counter

command_counter = Counter(
    'cqrs_commands_total',
    'Total commands processed',
    ['command_type', 'requested_by']
)

async def handle(self, command: CreateInviteCommand):
    # Increment counter with business context
    command_counter.labels(
        command_type=type(command).__name__,
        requested_by=command.requested_by or "anonymous"
    ).inc()
    
    result = await self.repository.create(command)
    return result
```

Now in Prometheus/Grafana you can query:
```promql
# Commands per user
sum by (requested_by) (cqrs_commands_total)

# P95 latency by command type
histogram_quantile(0.95, cqrs_command_duration_seconds)
```

## Audit Trail for Compliance (SOC 2, HIPAA, PCI DSS)

### Using OpenTelemetry Span Events (2026 Best Practice)

```python
async def handle(self, command: CreateInviteCommand):
    with tracer.start_as_current_span("CreateInvite") as span:
        attach_cqrs_context(span, command)
        
        # Execute command
        result = await self.repository.create(command)
        
        # Record audit event
        span.add_event(
            "invite.created",
            attributes={
                # Compliance fields
                "audit.action": "CREATE_INVITE",
                "audit.actor": command.requested_by or "system",
                "audit.resource_type": "invite",
                "audit.resource_id": str(result.id),
                "audit.timestamp": command.requested_at.isoformat(),
                
                # Business context
                "audit.business_request_id": str(command.request_id),
                "audit.correlation_id": str(command.correlation_id) if command.correlation_id else None,
                
                # Data classification
                "compliance.data_classification": "PII",
                "compliance.contains_email": True,
                
                # Result
                "audit.result": "success",
            }
        )
        
        return result
```

This creates audit trail entries that:
- Automatically correlate with the originating request
- Are stored in your tracing backend
- Support compliance requirements
- Can be queried for reports

## Real-World Example: Full Integration

### Production Incident Investigation

**Step 1: User Reports Issue**
```
"My order ORDER-12345 failed 10 minutes ago" - john@example.com
```

**Step 2: Search Application Logs (BaseCommand Fields)**
```bash
grep "requested_by=john@example.com" logs.txt | grep "ORDER-12345"

[550e8400-...] CreateOrderCommand | order_id=ORDER-12345 | 
  requested_by=john@example.com | at=2026-02-26 10:20:45
```

**Step 3: Use request_id to Find OTel Trace in Sentry**
```bash
# Search Sentry for: business.request_id=550e8400-...
```

**Step 4: See Full Distributed Trace**
```
Trace: abc123def456...
├─ HTTP POST /orders [200ms]
├─ CreateOrderCommand [business.request_id: 550e8400] [150ms]
│  ├─ ValidatePayment [50ms] ✅
│  ├─ CheckInventory [30ms] ✅
│  └─ SaveOrder [70ms] ❌ DATABASE_ERROR
└─ HTTP Response [500] ❌

Error: Connection timeout to postgres
Sentry Context:
  - requested_by: john@example.com
  - business.request_id: 550e8400-...
  - order.id: ORDER-12345
```

**Result:** 
- Found the exact user's request via **your domain fields**
- Saw the full technical trace via **OpenTelemetry**
- Diagnosed root cause: Database connection issue

**Without your BaseCommand fields:** You'd search through 1000s of traces with no business context.

## Complete Handler Example

Here's a production-ready handler with full observability:

```python
from opentelemetry import trace, baggage
from prometheus_client import Histogram, Counter
import sentry_sdk
from python_cqrs_core import BaseCommand, ICommandHandler

class CreateInviteCommand(BaseCommand):
    email: str
    expires_in_days: int

class CreateInviteHandler(ICommandHandler[CreateInviteCommand, InviteResult]):
    def __init__(self, repository, metrics_registry):
        self.repository = repository
        self.tracer = trace.get_tracer("cqrs.write", "1.0.0")
        
        # Prometheus metrics
        self.duration_histogram = Histogram(
            'create_invite_duration_seconds',
            'CreateInvite command duration',
            ['requested_by', 'status']
        )
        self.counter = Counter(
            'create_invite_total',
            'Total CreateInvite commands',
            ['requested_by']
        )
    
    async def handle(self, command: CreateInviteCommand) -> InviteResult:
        # Set up correlation
        correlation_id = str(command.correlation_id or command.request_id)
        ctx = baggage.set_baggage("correlation.id", correlation_id)
        
        status = "success"
        
        with self.tracer.start_as_current_span(
            "CreateInvite", 
            context=ctx
        ) as span:
            try:
                # Attach business context to OTel span
                span.set_attribute("business.request_id", str(command.request_id))
                span.set_attribute("requested_by", command.requested_by or "anonymous")
                span.set_attribute("cqrs.type", "command")
                span.set_attribute("cqrs.command.type", "CreateInvite")
                span.set_attribute("invite.email", command.email)
                
                # Attach context to Sentry
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag("business.request_id", str(command.request_id))
                    scope.set_tag("requested_by", command.requested_by)
                    scope.set_context("command", {
                        "type": "CreateInviteCommand",
                        "request_id": str(command.request_id),
                        "email": command.email,
                    })
                
                # Increment Prometheus counter
                self.counter.labels(
                    requested_by=command.requested_by or "anonymous"
                ).inc()
                
                # Execute business logic
                result = await self.repository.create(command)
                
                # Record audit event
                span.add_event(
                    "invite.created",
                    attributes={
                        "audit.action": "CREATE_INVITE",
                        "audit.actor": command.requested_by or "system",
                        "audit.resource_id": str(result.id),
                        "audit.timestamp": command.requested_at.isoformat(),
                    }
                )
                
                return result
                
            except Exception as e:
                status = "error"
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise
            
            finally:
                # Record duration in Prometheus
                duration = (datetime.now(timezone.utc) - command.requested_at).total_seconds()
                self.duration_histogram.labels(
                    requested_by=command.requested_by or "anonymous",
                    status=status
                ).observe(duration)
```

## Best Practices (2026)

### 1. Use Separate Tracers for Commands and Queries

```python
# Application setup
write_tracer = trace.get_tracer("cqrs.write", "1.0.0")
read_tracer = trace.get_tracer("cqrs.read", "1.0.0")

# Command handlers
class MyCommandHandler:
    tracer = write_tracer

# Query handlers
class MyQueryHandler:
    tracer = read_tracer
```

This enables independent performance analysis of read vs write paths.

### 2. Propagate Business Correlation IDs

Always set correlation IDs in baggage:

```python
correlation_id = str(command.correlation_id or command.request_id)
ctx = baggage.set_baggage("correlation.id", correlation_id)

with tracer.start_as_current_span("MyOperation", context=ctx):
    # Downstream services automatically get correlation.id
    await self.external_service.call()
```

### 3. Structure Audit Events Consistently

Use a consistent schema for all audit events:

```python
AUDIT_EVENT_SCHEMA = {
    "audit.action": "string",           # CREATE_USER, DELETE_ORDER, etc.
    "audit.actor": "string",            # Who (from requested_by)
    "audit.resource_type": "string",    # What type (user, order, invite)
    "audit.resource_id": "string",      # Which one (user_id, order_id)
    "audit.timestamp": "ISO8601",       # When (from requested_at)
    "audit.business_request_id": "UUID", # Unique identifier
    "audit.result": "string",           # success, denied, error
}
```

### 4. Use request_id for Log Correlation

Structure your logs to include request_id:

```python
import logging
import structlog

logger = structlog.get_logger()

async def handle(self, command: CreateInviteCommand):
    # Bind request_id to all logs in this context
    log = logger.bind(
        request_id=str(command.request_id),
        requested_by=command.requested_by,
        command_type=type(command).__name__
    )
    
    log.info("processing_command")
    result = await self.repository.create(command)
    log.info("command_completed", invite_id=result.id)
    
    return result
```

## Query Examples

### Find All Operations by User

**Application logs:**
```bash
grep 'requested_by=john@example.com' app.log
```

**Sentry:**
```
Search: requested_by:"john@example.com"
```

**Jaeger (OpenTelemetry):**
```
Tags: requested_by="john@example.com"
```

### Trace Request Flow

**Using correlation_id:**
```bash
# Find initial request
grep 'request_id=550e8400' app.log

# Find all related operations
grep 'correlation_id=550e8400' app.log
```

**In Jaeger:**
```
Search by baggage: correlation.id="550e8400..."
→ Shows all connected operations across services
```

## Summary: Why Keep BaseQuery/BaseCommand with OTel/Sentry?

### They Solve Different Problems

| Problem | Solution |
|---------|----------|
| **"Which request failed?"** | `request_id` (yours) |
| **"Where in the code did it fail?"** | OpenTelemetry spans |
| **"Who made this request?"** | `requested_by` (yours) |
| **"What was the error?"** | Sentry error tracking |
| **"How long did it take?"** | Both (`requested_at` + OTel timing) |
| **"What's the related operation?"** | `correlation_id` (yours) + OTel baggage |

### Your Fields Are the Bridge

```
User Reports Issue
  ↓
Search by business context (requested_by, order_id)
  ↓ [YOUR FIELDS]
Find request_id in logs
  ↓
Search Sentry/Jaeger by business.request_id
  ↓ [INFRASTRUCTURE TOOLS]
View full distributed trace
  ↓
Diagnose technical root cause
```

**Without your BaseCommand fields:** Infrastructure tools have no business context.  
**Without infrastructure tools:** Your fields have no technical details.

**Together:** Complete observability from business to infrastructure! 🎯
