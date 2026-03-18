"""Unit tests for IOutboxEvent interface.

Tests event contract and behavior.
RULE: Maximum 100 lines per file.
"""

from datetime import datetime, timezone
from uuid import uuid4, UUID
from python_outbox_core import IOutboxEvent


class ConcreteEvent(IOutboxEvent):
    """Concrete implementation for testing."""
    
    user_name: str
    
    def to_message(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "data": {"user_name": self.user_name}
        }


def test_event_creation():
    """Should create event with required fields."""
    event_id = uuid4()
    now = datetime.now(timezone.utc)
    
    event = ConcreteEvent(
        event_id=event_id,
        event_type="user.created",
        aggregate_id="user-123",
        occurred_at=now,
        source="user-service",
        user_name="John Doe"
    )
    
    assert event.event_id == event_id
    assert event.event_type == "user.created"
    assert event.aggregate_id == "user-123"
    assert event.occurred_at == now
    assert event.source == "user-service"
    assert event.user_name == "John Doe"


def test_event_default_data_version():
    """Should use default data version."""
    event = ConcreteEvent(
        event_id=uuid4(),
        event_type="user.created",
        aggregate_id="user-123",
        occurred_at=datetime.now(timezone.utc),
        source="user-service",
        user_name="John"
    )
    
    assert event.data_version == "1.0"


def test_event_optional_fields():
    """Should handle optional correlation and causation IDs."""
    corr_id = uuid4()
    cause_id = uuid4()
    
    event = ConcreteEvent(
        event_id=uuid4(),
        event_type="user.updated",
        aggregate_id="user-456",
        occurred_at=datetime.now(timezone.utc),
        source="user-service",
        user_name="Jane",
        correlation_id=corr_id,
        causation_id=cause_id
    )
    
    assert event.correlation_id == corr_id
    assert event.causation_id == cause_id


def test_event_get_partition_key():
    """Should use aggregate_id as default partition key."""
    event = ConcreteEvent(
        event_id=uuid4(),
        event_type="user.created",
        aggregate_id="user-789",
        occurred_at=datetime.now(timezone.utc),
        source="user-service",
        user_name="Bob"
    )
    
    assert event.get_partition_key() == "user-789"


def test_event_to_message():
    """Should serialize to message format."""
    event_id = uuid4()
    event = ConcreteEvent(
        event_id=event_id,
        event_type="user.created",
        aggregate_id="user-111",
        occurred_at=datetime.now(timezone.utc),
        source="user-service",
        user_name="Alice"
    )
    
    message = event.to_message()
    
    assert message["event_id"] == str(event_id)
    assert message["event_type"] == "user.created"
    assert message["aggregate_id"] == "user-111"
    assert message["data"]["user_name"] == "Alice"
