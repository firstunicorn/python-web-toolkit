# Outbox Core - API Quick Reference

**Version:** 0.1.0 | **Status:** ✅ Production Ready

---

## 📦 Installation

```bash
pip install outbox-sdk
# or
poetry add outbox-sdk
```

---

## 🔌 Core API

### Events

```python
from outbox_sdk.core import IOutboxEvent

class IOutboxEvent(BaseModel, ABC):
    # Required
    event_id: UUID
    event_type: str                   # "com.company.domain.action"
    aggregate_id: str
    occurred_at: datetime
    source: str                       # Service name

    # Versioning
    data_version: str = "1.0"

    # Tracing (optional)
    correlation_id: UUID | None
    causation_id: UUID | None

    @abstractmethod
    def to_message(self) -> dict[str, Any]:
        """Convert to broker format."""
```

---

### Repository

```python
from outbox_sdk.core import IOutboxRepository

class IOutboxRepository(ABC):
    async def add_event(event: IOutboxEvent) -> None
    async def get_unpublished(limit: int = 100, offset: int = 0) -> List[IOutboxEvent]
    async def mark_published(event_id: UUID) -> None
    async def mark_failed(event_id: UUID, error_message: str) -> None
    async def count_unpublished() -> int
```

---

### Publisher

```python
from outbox_sdk.core import IEventPublisher

class IEventPublisher(ABC):
    async def publish(message: dict[str, Any]) -> None
```

---

### Worker

```python
from outbox_sdk.core import OutboxPublisherBase

class OutboxPublisherBase(ABC):
    def __init__(
        repository: IOutboxRepository,
        publisher: IEventPublisher,
        error_handler: OutboxErrorHandler | None = None,
        metrics: OutboxMetrics | None = None,
    )

    async def publish_batch(limit: int = 100) -> int

    @abstractmethod
    async def schedule_publishing() -> None
```

---

### Error Handling

```python
from outbox_sdk.core import OutboxErrorHandler

class OutboxErrorHandler:
    def __init__(logger: Any = None, max_retries: int = 3)

    def handle(event: Any, exception: Exception) -> None
    def should_retry(event: Any, exception: Exception, attempt: int) -> bool
    def is_transient_error(exception: Exception) -> bool
```

---

### Metrics

```python
from outbox_sdk.core import OutboxMetrics

class OutboxMetrics:
    def __init__(logger: Any = None)

    def log_no_events() -> None
    def log_success(event: Any) -> None
    def log_batch_complete(published: int, total: int) -> None
    def log_batch_started(batch_size: int) -> None
```

---

### Configuration

```python
from outbox_sdk.core import OutboxConfig

class OutboxConfig(BaseModel):
    batch_size: int = 100                  # 1-1000
    poll_interval_seconds: int = 5         # 1-3600
    max_retry_count: int = 3               # 0-100
    retry_backoff_multiplier: float = 2.0  # 1.0-10.0
    enable_metrics: bool = True
    enable_health_check: bool = True

    # Env vars: OUTBOX_BATCH_SIZE, OUTBOX_POLL_INTERVAL_SECONDS, etc.
```

---

### Health Checks

```python
from outbox_sdk.core import OutboxHealthCheck, HealthStatus

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class OutboxHealthCheck(ABC):
    async def check_health() -> Dict[str, Any]
    async def check_database() -> Dict[str, Any]
    async def check_broker() -> Dict[str, Any]
    async def check_outbox_lag() -> Dict[str, Any]
```

---

### Serialization

**NOTE:** No custom serializer!

**💡 RECOMMENDED:** [FastStream](https://faststream.airt.ai/) (ag2ai) - cutting-edge event-driven framework, especially for startups. Custom serializers supported if needed.

In most cases just use Pydantic v2 built-in methods:

```python
# Serialize to JSON string (for PostgreSQL JSONB)
json_str = event.model_dump_json()

# Deserialize from JSON string
event = UserCreatedEvent.model_validate_json(json_str)

# For Kafka: FastStream auto-serializes dicts!
await broker.publish(event.to_message())  # No manual JSON needed
```

---

## 🚀 Quick Start

### 1. Define Event

```python
from outbox_sdk.core import IOutboxEvent
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field

class UserCreatedEvent(IOutboxEvent):
    user_id: UUID
    email: str

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = "com.app.user.created"
    aggregate_id: str = Field(alias="user_id")
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = "user-service"

    def to_message(self) -> dict:
        return {
            "id": str(self.event_id),
            "type": self.event_type,
            "data": {"user_id": str(self.user_id), "email": self.email}
        }
```

### 2. Store in Transaction

```python
async def create_user(cmd, user_repo, outbox_repo, db_session):
    user = await user_repo.create(cmd.to_entity())
    event = UserCreatedEvent(user_id=user.id, email=user.email)
    await outbox_repo.add_event(event)
    await db_session.commit()  # Atomic!
```

### 3. Implement Worker

```python
from outbox_sdk.core import OutboxPublisherBase
import asyncio

class MyWorker(OutboxPublisherBase):
    async def schedule_publishing(self):
        while True:
            await self.publish_batch(limit=100)
            await asyncio.sleep(5)
```

### 4. Implement Repository

```python
from outbox_sdk.core import IOutboxRepository
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyOutboxRepo(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_event(self, event):
        orm_event = OutboxEventORM(
            id=event.event_id,
            event_type=event.event_type,
            payload=event.model_dump_json(),  # Pydantic built-in!
            # ...
        )
        self.session.add(orm_event)
        # No commit - caller handles!

    async def get_unpublished(self, limit=100, offset=0):
        result = await self.session.execute(
            select(OutboxEventORM)
            .where(OutboxEventORM.published == False)
            .order_by(OutboxEventORM.occurred_at.asc())
            .limit(limit)
        )
        # Deserialize using Pydantic built-in
        events = []
        for orm in result.scalars().all():
            event_class = self.event_registry[orm.event_type]
            events.append(event_class.model_validate_json(orm.payload))
        return events

    async def mark_published(self, event_id):
        await self.session.execute(
            update(OutboxEventORM)
            .where(OutboxEventORM.id == event_id)
            .values(published=True, published_at=datetime.utcnow())
        )

    async def mark_failed(self, event_id, error_message):
        await self.session.execute(
            update(OutboxEventORM)
            .where(OutboxEventORM.id == event_id)
            .values(failed=True, error_message=error_message)
        )

    async def count_unpublished(self):
        result = await self.session.execute(
            select(func.count(OutboxEventORM.id))
            .where(OutboxEventORM.published == False)
        )
        return result.scalar()
```

### 5. Implement Publisher

```python
from outbox_sdk.core import IEventPublisher
from faststream.kafka import KafkaBroker

class KafkaPublisher(IEventPublisher):
    def __init__(self, broker: KafkaBroker):
        self.broker = broker

    async def publish(self, message: dict):
        # NOTE: FastStream auto-serializes dict → JSON!
        await self.broker.publish(
            message,
            topic=message.get("type"),
            key=message.get("aggregate_id")
        )
```

---

## 🎯 Full Import Example

```python
from outbox_sdk.core import (
    # Contracts
    IOutboxEvent,
    IOutboxRepository,
    IEventPublisher,

    # Worker
    OutboxPublisherBase,
    OutboxErrorHandler,
    OutboxMetrics,

    # Utils
    OutboxConfig,

    # Health
    OutboxHealthCheck,
    HealthStatus,
)

# NOTE: No OutboxSerializer - use Pydantic's model_dump_json() instead!
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Command Handler                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 1. Create domain entity                             │ │
│ │ 2. Save entity (user_repo.save)                     │ │
│ │ 3. Create event (UserCreatedEvent)                  │ │
│ │ 4. Store event (outbox_repo.add_event)             │ │
│ │ 5. db_session.commit() ← ATOMIC!                    │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Database (PostgreSQL)                                   │
│ ┌──────────────┐  ┌──────────────────────────────────┐ │
│ │ users table  │  │ outbox_events table              │ │
│ │ (domain)     │  │ - id, event_type, payload        │ │
│ │              │  │ - published (false → true)       │ │
│ └──────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Background Worker (OutboxPublisherBase)                 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Every 5s:                                           │ │
│ │ 1. Fetch unpublished (outbox_repo.get_unpublished) │ │
│ │ 2. Publish to Kafka (publisher.publish)            │ │
│ │ 3. Mark published (outbox_repo.mark_published)     │ │
│ │ 4. Handle errors (error_handler.handle)            │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Kafka / Message Broker                                  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Topic: com.app.user.created                         │ │
│ │ Message: {"id": "...", "data": {...}}               │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Consumers (Other Services)                              │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Key Guarantees

| Guarantee | How? |
|-----------|------|
| **Atomicity** | Domain entity + outbox event in same DB transaction |
| **At-least-once delivery** | Events persisted before publishing |
| **No message loss** | Events durable in DB, retried on failure |
| **Idempotency** | `event_id` as idempotency key |
| **FIFO ordering** | Per-aggregate via `occurred_at ASC` |
| **Dead Letter Queue** | `mark_failed()` for permanent failures |

---

## 🔧 Configuration via Environment

```bash
export OUTBOX_BATCH_SIZE=200
export OUTBOX_POLL_INTERVAL_SECONDS=10
export OUTBOX_MAX_RETRY_COUNT=5
export OUTBOX_ENABLE_METRICS=true
```

```python
from outbox_sdk.core import OutboxConfig

config = OutboxConfig()  # Auto-loads from env
print(config.batch_size)  # 200
```

---

## 📈 Monitoring

### Health Check Endpoint

```python
from fastapi import FastAPI
from outbox_sdk.core import OutboxHealthCheck, HealthStatus

class MyHealthCheck(OutboxHealthCheck):
    async def check_health(self):
        return {
            "status": HealthStatus.HEALTHY,
            "checks": {
                "database": await self.check_database(),
                "broker": await self.check_broker(),
                "outbox_lag": await self.check_outbox_lag(),
            }
        }

app = FastAPI()
health_check = MyHealthCheck()

@app.get("/health")
async def health():
    return await health_check.check_health()
```

### Structured Logs

```json
{
  "event": "outbox.event_published",
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "com.app.user.created",
  "aggregate_id": "user-123",
  "timestamp": "2024-01-01T12:00:00Z"
}

{
  "event": "outbox.batch_complete",
  "published": 95,
  "total": 100,
  "success_rate": 0.95,
  "timestamp": "2024-01-01T12:00:05Z"
}
```

---

## 🧪 Testing

### Mock Repository

```python
class InMemoryOutboxRepo(IOutboxRepository):
    def __init__(self):
        self.events = []

    async def add_event(self, event):
        self.events.append(event)

    async def get_unpublished(self, limit=100, offset=0):
        return [e for e in self.events if not e.published][:limit]
```

### Mock Publisher

```python
class FakePublisher(IEventPublisher):
    def __init__(self):
        self.published_messages = []

    async def publish(self, message):
        self.published_messages.append(message)
```

### Unit Test

```python
async def test_outbox_worker():
    repo = InMemoryOutboxRepo()
    publisher = FakePublisher()
    worker = MyWorker(repo, publisher)

    await repo.add_event(UserCreatedEvent(...))

    published_count = await worker.publish_batch()

    assert published_count == 1
    assert len(publisher.published_messages) == 1
```

---

## 📚 See Also

- **Full API Docs:** [`CORE_API.md`](./CORE_API.md)
- **CloudEvents Spec:** https://cloudevents.io/
- **Transactional Outbox:** [`../../architecture/06_EVENT_PATTERNS.md`](../../architecture/06_EVENT_PATTERNS.md)

---

**Lines of Code:** 732 total | **Files:** 9 | **Avg:** 81 lines/file

