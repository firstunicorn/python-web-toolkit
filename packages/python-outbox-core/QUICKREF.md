# Outbox Core - Quick Reference

**NOTE:** No custom serializer! Use Pydantic's `model_dump_json()` & `model_validate_json()`. FastStream auto-serializes dicts.

**💡 RECOMMENDED:** FastStream (ag2ai) - cutting-edge for event-driven systems, ideal for startups. Custom serializers welcome.

## API

```python
# Event
class IOutboxEvent(BaseModel, ABC):
    event_id: UUID; event_type: str; aggregate_id: str
    occurred_at: datetime; source: str; data_version: str = "1.0"
    @abstractmethod
    def to_message(self) -> dict: ...

# Repository
class IOutboxRepository(ABC):
    async def add_event(event) -> None
    async def get_unpublished(limit=100) -> List[IOutboxEvent]
    async def mark_published(event_id: UUID) -> None
    async def mark_failed(event_id: UUID, error: str) -> None

# Publisher
class IEventPublisher(ABC):
    async def publish(message: dict) -> None  # FastStream handles JSON!

# Worker
class OutboxPublisherBase(ABC):
    async def publish_batch(limit=100) -> int
    @abstractmethod
    async def schedule_publishing() -> None
```

## Usage

```python
# 1. Define
class UserCreated(IOutboxEvent):
    user_id: UUID; email: str
    event_type: str = "user.created"; source: str = "api"
    def to_message(self): return {"id": str(self.event_id), "data": {...}}

# 2. Store (atomic with domain entity)
await outbox_repo.add_event(UserCreated(...))
await db_session.commit()

# 3. Worker
class Worker(OutboxPublisherBase):
    async def schedule_publishing(self):
        while True: await self.publish_batch(); await asyncio.sleep(5)

# 4. Repository (SQLAlchemy)
class Repo(IOutboxRepository):
    async def add_event(self, e):
        self.session.add(OutboxORM(
            id=e.event_id,
            payload=e.model_dump_json()  # Pydantic built-in!
        ))
    async def get_unpublished(self, limit=100):
        result = await self.session.execute(
            select(OutboxORM).where(OutboxORM.published==False).limit(limit)
        )
        return [EventClass.model_validate_json(orm.payload) for orm in result.scalars()]

# 5. Publisher (Kafka via FastStream)
class KafkaPub(IEventPublisher):
    async def publish(self, msg):
        # FastStream auto-serializes dict → JSON!
        await self.broker.publish(msg, topic=msg["type"])
```

## Config (Env)

```bash
OUTBOX_BATCH_SIZE=100
OUTBOX_POLL_INTERVAL_SECONDS=5
```

## Import

```python
from outbox_sdk.core import (
    IOutboxEvent, IOutboxRepository, IEventPublisher,
    OutboxPublisherBase, OutboxConfig, OutboxErrorHandler, OutboxMetrics
)
```

## Serialization Notes

**No custom serializer needed!**
- **DB Storage:** Use `event.model_dump_json()` (Pydantic v2)
- **DB Loading:** Use `EventClass.model_validate_json(json_str)` (Pydantic v2)
- **Kafka Publishing:** FastStream auto-serializes `dict` → JSON

## Pattern

```
Handler → DB(entity + outbox) → Worker → Kafka
         └──── ATOMIC ────┘
```

✅ Atomic | ✅ At-least-once | ✅ No loss | ✅ DLQ

