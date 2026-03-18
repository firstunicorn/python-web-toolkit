"""Property-based tests for InProcessEventDispatcher."""

import pytest
from hypothesis import given, strategies as st
from python_domain_events import (
    BaseDomainEvent,
    IDomainEventHandler,
    InProcessEventDispatcher
)


class SampleEvent(BaseDomainEvent):
    """Sample event for dispatcher tests."""
    event_type: str = "test.event"
    data: str


class MockEventHandler(IDomainEventHandler[SampleEvent]):
    """Mock handler that records handled events."""
    
    def __init__(self):
        self.handled_events = []
    
    async def handle(self, event: SampleEvent) -> None:
        self.handled_events.append(event)


@given(st.text(min_size=1))
@pytest.mark.asyncio
async def test_dispatcher_routes_event_to_handler(data: str):
    """Should route event to registered handler."""
    dispatcher = InProcessEventDispatcher()
    handler = MockEventHandler()
    
    dispatcher.register(SampleEvent, handler)
    
    event = SampleEvent(data=data)
    await dispatcher.dispatch(event)
    
    assert len(handler.handled_events) == 1
    assert handler.handled_events[0] == event


@given(st.text(min_size=1))
@pytest.mark.asyncio
async def test_dispatcher_routes_to_multiple_handlers(data: str):
    """Should route event to all registered handlers."""
    dispatcher = InProcessEventDispatcher()
    handler1 = MockEventHandler()
    handler2 = MockEventHandler()
    
    dispatcher.register(SampleEvent, handler1)
    dispatcher.register(SampleEvent, handler2)
    
    event = SampleEvent(data=data)
    await dispatcher.dispatch(event)
    
    assert len(handler1.handled_events) == 1
    assert len(handler2.handled_events) == 1


@given(st.text(min_size=1))
@pytest.mark.asyncio
async def test_dispatcher_clear_removes_handlers(data: str):
    """Should clear all registered handlers."""
    dispatcher = InProcessEventDispatcher()
    handler = MockEventHandler()
    
    dispatcher.register(SampleEvent, handler)
    dispatcher.clear()
    
    event = SampleEvent(data=data)
    await dispatcher.dispatch(event)
    
    assert len(handler.handled_events) == 0


@given(st.text(min_size=1))
@pytest.mark.asyncio
async def test_dispatcher_propagates_handler_exceptions(data: str):
    """Should propagate exceptions from handlers."""
    
    class FailingHandler(IDomainEventHandler[SampleEvent]):
        async def handle(self, event: SampleEvent) -> None:
            raise ValueError("Handler failed")
    
    dispatcher = InProcessEventDispatcher()
    dispatcher.register(SampleEvent, FailingHandler())
    
    event = SampleEvent(data=data)
    
    with pytest.raises(ValueError):
        await dispatcher.dispatch(event)
