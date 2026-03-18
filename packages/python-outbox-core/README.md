# Python Outbox Core

**Core abstractions for implementing the Transactional Outbox pattern with Kafka/FastStream**

## 📦 What is this?

This library provides framework-agnostic base classes and interfaces for implementing the [Transactional Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html), ensuring atomic writes to your database and reliable event publishing.

## 🎯 Problem Solved

**The Dual Write Problem:**
- Writing to DB + Publishing to Kafka = **Two separate systems**
- If app crashes between the two → **Event lost**
- If Kafka is down → **Event lost**
- Result: **Inconsistent state**

**The Outbox Solution:**
1. Store events in outbox table (same DB transaction as your domain changes)
2. Background worker publishes events to Kafka asynchronously
3. ✅ **Atomic:** DB writes + event storage in single transaction
4. ✅ **Durable:** Events never lost (stored in DB)
5. ✅ **Reliable:** Publishing retries handled separately

---

## 🔀 When to Use This Library?

**Use IOutboxEvent (this library) for:**
- 🌐 **Cross-service communication** (other microservices need to react)
- 🌐 **External integrations** (analytics, audit services, third-party)
- 🌐 **Event-driven architecture** (Kafka, message brokers)
- 🌐 **Guaranteed delivery** (at-least-once semantics)

**Do NOT use for:**
- 🔷 **In-process events** (use `BaseDomainEvent` from `python-domain-primitives`)
- 🔷 **Same service side effects** (send email, update cache within same service)
- 🔷 **Direct function calls** (no message broker needed)

### Event Type Decision Tree

```
Need to publish an event?
│
├─ Same service only?
│  └─ Use BaseDomainEvent (python-domain-primitives)
│     Examples: Send email, log activity, update cache
│
└─ Other services/external?
   └─ Use IOutboxEvent (python-outbox-core) ⭐ THIS LIBRARY
      Examples: Notify microservices, analytics, audit
```

**Related Libraries:**
- 🔷 **`python-domain-primitives`** - For internal domain events (`BaseDomainEvent`)
- 🌐 **`python-outbox-core`** - For external integration events (`IOutboxEvent`) ⭐ YOU ARE HERE
- 🔧 **`python-outbox-fastapi`** - FastAPI lifespan helpers
- 🔧 **`python-outbox-celery`** - Celery background workers
- 🔧 **`python-outbox-faststream`** - Kafka/FastStream publishers

## 🏗️ What's Included

### Core Abstractions

```python
from python_outbox_core import IOutboxEvent, IOutboxRepository, OutboxPublisherBase

# 1. Event Interface
class MyDomainEvent(IOutboxEvent):
    """Your domain events implement this interface."""
    pass

# 2. Repository Interface
class MyOutboxRepo(IOutboxRepository):
    """Your SQLAlchemy repository implements this."""
    pass

# 3. Publisher Base Class
class MyOutboxWorker(OutboxPublisherBase):
    """Your background worker extends this."""
    pass
```

## 📚 Components

| Component | Purpose | LOC |
|-----------|---------|-----|
| `IOutboxEvent` | Base interface for outbox events with metadata | ~20 |
| `IOutboxRepository` | Repository contract for outbox persistence | ~25 |
| `OutboxPublisherBase` | Reusable publishing logic for workers | ~40 |

**NOTE:** No custom serializer! Use Pydantic's `model_dump_json()` & FastStream's auto-serialization.

**💡 RECOMMENDED:** [FastStream](https://faststream.airt.ai/) (by ag2ai) - cutting-edge event-driven framework, ideal for startups. Or implement custom serializers as needed.

## 🔧 Tech Stack Integration

- **SQLAlchemy** - For ORM models and async sessions
- **Kafka** - Event streaming platform
- **FastStream** - High-level Kafka abstraction
- **Kong Events Gateway** - API gateway for event routing

## 📖 Usage Example

```python
from python_outbox_core import IOutboxEvent, IOutboxRepository, OutboxPublisherBase
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

# 1. Define your domain event
class InviteCreatedEvent(BaseModel, IOutboxEvent):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = "invite.created"
    aggregate_id: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    # Domain-specific payload
    email: str
    role: str

    def to_message(self) -> dict:
        return self.model_dump(mode='json')

# 2. Implement repository (your SQLAlchemy code)
class OutboxRepository(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_event(self, event: IOutboxEvent) -> None:
        outbox_record = OutboxEventModel(**event.to_message())
        self.session.add(outbox_record)

    # ... implement other methods

# 3. Create background worker
class KafkaOutboxWorker(OutboxPublisherBase):
    async def schedule_publishing(self) -> None:
        while True:
            published = await self.publish_batch(limit=100)
            await asyncio.sleep(5)  # Poll every 5 seconds
```

## 🚀 Installation

```bash
cd C:\coding\gridflow
pip install -e ./python-web-toolkit/packages/python-outbox-core
```

## 🔗 Related Libraries

- `sqlalchemy-async-repositories` - Base repository patterns
- `python-infrastructure-exceptions` - Infrastructure errors
- `python-structlog-config` - Structured logging with OTel

## 📄 License

MIT

## 🤝 Contributing

This is part of the GridFlow python-web-toolkit monorepo. Follow the 100-line file limit rule.

