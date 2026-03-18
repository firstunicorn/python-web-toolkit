"""Property-based tests for BaseDomainEvent."""

import pytest
from datetime import datetime
from uuid import UUID
from hypothesis import given, strategies as st
from python_domain_events import BaseDomainEvent


class SampleEvent(BaseDomainEvent):
    """Sample event for testing."""
    event_type: str = "test.event"
    data: str


@given(st.text(min_size=1))
def test_event_creation_generates_event_id(data: str):
    """Should auto-generate unique event_id."""
    event = SampleEvent(data=data)
    assert isinstance(event.event_id, UUID)


@given(st.text(min_size=1))
def test_event_creation_generates_occurred_at(data: str):
    """Should auto-generate occurred_at timestamp."""
    event = SampleEvent(data=data)
    assert isinstance(event.occurred_at, datetime)


@given(st.text(min_size=1))
def test_event_ids_are_unique(data: str):
    """Should generate unique event_id for each event."""
    event1 = SampleEvent(data=data)
    event2 = SampleEvent(data=data)
    assert event1.event_id != event2.event_id


@given(st.text(min_size=1))
def test_event_is_immutable(data: str):
    """Should be immutable after creation."""
    event = SampleEvent(data=data)
    with pytest.raises(Exception):
        event.data = "modified"


@given(st.text(min_size=1), st.uuids())
def test_event_with_correlation_id(data: str, correlation_id: UUID):
    """Should accept correlation_id for distributed tracing."""
    event = SampleEvent(data=data, correlation_id=correlation_id)
    assert event.correlation_id == correlation_id


@given(st.text(min_size=1), st.uuids(), st.uuids())
def test_event_with_causation_id(data: str, correlation_id: UUID, causation_id: UUID):
    """Should accept causation_id for event chains."""
    event = SampleEvent(
        data=data,
        correlation_id=correlation_id,
        causation_id=causation_id
    )
    assert event.causation_id == causation_id


@given(st.text(min_size=1), st.dictionaries(st.text(), st.text()))
def test_event_with_metadata(data: str, metadata: dict):
    """Should accept custom metadata."""
    event = SampleEvent(data=data, metadata=metadata)
    assert event.metadata == metadata


@given(st.text(min_size=1))
def test_event_serialization(data: str):
    """Should serialize to JSON."""
    event = SampleEvent(data=data)
    json_str = event.model_dump_json()
    assert isinstance(json_str, str)
    # Verify event can be serialized and data field exists
    assert '"data"' in json_str
