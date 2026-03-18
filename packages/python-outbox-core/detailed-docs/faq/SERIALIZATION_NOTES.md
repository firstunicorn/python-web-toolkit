# Serialization Notes

## ❓ Why No Custom Serializer?

**Short answer:** Pydantic v2 and FastStream already handle everything.

---

## 🔍 What Each Technology Does

### ✅ **Pydantic v2 (Built-in)**

```python
# Serialize to JSON string
json_str = event.model_dump_json()  # Handles UUID, datetime, etc.

# Deserialize from JSON string
event = UserCreatedEvent.model_validate_json(json_str)
```

**Handles:**
- UUID → string
- datetime → ISO 8601
- Decimal → float
- Nested models
- Field validation

---

### ✅ **FastStream (Auto-Serializes)**

```python
from faststream.kafka import KafkaBroker

broker = KafkaBroker()

# FastStream auto-converts dict → JSON!
await broker.publish(
    {"user_id": "123", "email": "test@example.com"},
    topic="events"
)
```

**Handles:**
- dict → JSON string
- Kafka message encoding
- Content-Type headers

---

### ⚠️ **When You DO Need Serialization**

Only for **PostgreSQL JSONB storage**:

```python
# Store to DB
payload = event.model_dump_json()  # Pydantic built-in
orm = OutboxEventORM(id=event.event_id, payload=payload)
session.add(orm)

# Load from DB
event = UserCreatedEvent.model_validate_json(orm.payload)  # Pydantic built-in
```

---

## 🎯 Pattern Summary

```
Command Handler
    ↓
event.model_dump_json()  ← Store to PostgreSQL
    ↓
PostgreSQL JSONB
    ↓
EventClass.model_validate_json(json_str)  ← Load from DB
    ↓
event.to_message() → dict
    ↓
broker.publish(dict)  ← FastStream auto-serializes!
    ↓
Kafka (JSON)
```

---

## 🚨 Common Mistakes

### ❌ **Don't do this:**

```python
# BAD: Manual JSON encoding
import json
payload = json.dumps(event.dict())  # Breaks UUID, datetime!

# BAD: Custom serializer
class MySerializer:
    def serialize(self, event): ...  # Why reinvent Pydantic?
```

### ✅ **Do this:**

```python
# GOOD: Use Pydantic
payload = event.model_dump_json()
event = EventClass.model_validate_json(payload)
```

---

## 📋 Serialization Matrix

| Operation | Tool | Method |
|-----------|------|--------|
| **Event → PostgreSQL** | Pydantic | `event.model_dump_json()` |
| **PostgreSQL → Event** | Pydantic | `EventClass.model_validate_json(str)` |
| **Event → Kafka** | FastStream | Auto (just pass dict) |
| **Kafka → Event** | FastStream | Auto (handler receives dict) |

---

## 🎯 Best Practices

1. **PostgreSQL Storage:** Always use `model_dump_json()` / `model_validate_json()`
2. **Kafka Publishing:** Let FastStream handle serialization (just pass `dict`)
3. **Custom Types:** Define Pydantic validators, not custom serializers
4. **Testing:** Mock with dicts, not JSON strings

---

## 🔧 Event Registry Pattern

For deserializing from DB, you need an event type registry:

```python
class EventRegistry:
    """Maps event_type string → Event class."""

    _registry: dict[str, type[IOutboxEvent]] = {
        "com.app.user.created": UserCreatedEvent,
        "com.app.user.deleted": UserDeletedEvent,
    }

    @classmethod
    def get(cls, event_type: str) -> type[IOutboxEvent]:
        return cls._registry[event_type]

# In Repository
def _deserialize(self, json_str: str) -> IOutboxEvent:
    data = json.loads(json_str)
    event_class = EventRegistry.get(data["event_type"])
    return event_class.model_validate_json(json_str)
```

---

**Bottom line:** No custom serializer needed. Pydantic + FastStream = complete solution. ✅

