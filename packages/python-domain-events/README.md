# Python Domain Events

**Base classes for internal domain events with distributed tracing support**

## 📦 What is this?

This library provides base classes for implementing internal domain events (in-process) that follow DDD best practices and support distributed tracing.

## 🎯 When to Use This Library?

**Use BaseDomainEvent (this library) for:**
- 🔷 **In-process events** (same service side effects)
- 🔷 **Internal coordination** (send email, update cache, log activity)
- 🔷 **Bounded context events** (within one microservice)
- 🔷 **Immediate processing** (synchronous event handling)

**Do NOT use for:**
- 🌐 **Cross-service communication** (use `IOutboxEvent` from `python-outbox-core`)
- 🌐 **External integrations** (analytics, audit services, third-party)
- 🌐 **Message broker events** (Kafka, RabbitMQ)

### Event Type Decision Tree

```
Need to publish an event?
│
├─ Same service only?
│  └─ Use BaseDomainEvent (python-domain-events) ⭐ THIS LIBRARY
│     Examples: Send email, log activity, update cache
│
└─ Other services/external?
   └─ Use IOutboxEvent (python-outbox-core)
      Examples: Notify microservices, analytics, audit
```

## 🚀 Quick Start

### Installation

```bash
pip install -e python-web-toolkit/packages/python-domain-events
```

### Basic Usage

```python
from python_domain_events import BaseDomainEvent
from uuid import UUID
from typing import Optional

class InviteCreatedEvent(BaseDomainEvent):
    """Domain event: Invite was created."""
    event_type: str = "invite.created"
    
    invite_id: int
    token: str
    email: Optional[str]
    
    @classmethod
    def from_entity(cls, invite, correlation_id: Optional[UUID] = None):
        return cls(
            invite_id=invite.id,
            token=invite.token,
            email=invite.email,
            correlation_id=correlation_id
        )

# Create event
event = InviteCreatedEvent.from_entity(invite)

# Event has auto-generated fields
print(event.event_id)        # UUID
print(event.occurred_at)     # datetime
print(event.correlation_id)  # Optional UUID for tracing
```

## 📚 Features

✅ **Auto-generated event_id** - UUID for deduplication  
✅ **Auto-generated timestamps** - No manual `datetime.utcnow()`  
✅ **Distributed tracing** - `correlation_id`, `causation_id` support  
✅ **Immutability** - Events are frozen after creation  
✅ **Type safety** - Full Pydantic validation  
✅ **Extensible metadata** - `metadata: Dict[str, Any]` for custom fields

## 🏗️ Components

- **BaseDomainEvent** - Base class for domain events
- **IDomainEventHandler** - Interface for event handlers
- **InProcessEventDispatcher** - Dispatcher for routing events to handlers

## 📖 License

MIT
