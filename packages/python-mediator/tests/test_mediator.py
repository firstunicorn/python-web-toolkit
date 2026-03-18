"""Unit tests for Mediator class.

Tests core mediator functionality including handler registration and dispatch.
RULE: Maximum 100 lines per file.
"""

import pytest
from python_mediator import Mediator


class SampleRequest:
    """Sample request for testing."""
    def __init__(self, value: str):
        self.value = value


class SampleHandler:
    """Sample handler for testing."""
    async def handle(self, request: SampleRequest) -> str:
        return f"Handled: {request.value}"


class AnotherRequest:
    """Another request for testing."""
    pass


def test_mediator_initialization():
    """Should initialize with empty handlers and behaviors."""
    mediator = Mediator()
    
    assert mediator._handlers == {}
    assert mediator._behaviors == []


def test_register_handler():
    """Should register handler for request type."""
    mediator = Mediator()
    handler = SampleHandler()
    
    mediator.register_handler(SampleRequest, handler)
    
    assert SampleRequest in mediator._handlers
    assert mediator._handlers[SampleRequest] is handler


def test_register_duplicate_handler_raises():
    """Should raise on duplicate handler registration."""
    mediator = Mediator()
    handler = SampleHandler()
    
    mediator.register_handler(SampleRequest, handler)
    
    with pytest.raises(ValueError, match="Handler already registered"):
        mediator.register_handler(SampleRequest, handler)


async def test_send_dispatches_to_handler():
    """Should dispatch request to registered handler."""
    mediator = Mediator()
    mediator.register_handler(SampleRequest, SampleHandler())
    
    result = await mediator.send(SampleRequest("test"))
    
    assert result == "Handled: test"


async def test_send_unregistered_raises():
    """Should raise on unregistered request type."""
    mediator = Mediator()
    
    with pytest.raises(ValueError, match="No handler registered"):
        await mediator.send(AnotherRequest())


async def test_add_pipeline_behavior():
    """Should execute pipeline behaviors before handler."""
    mediator = Mediator()
    mediator.register_handler(SampleRequest, SampleHandler())
    
    called = []
    
    async def logging_behavior(request, handler):
        called.append("behavior")
        return None  # Continue to handler
    
    mediator.add_pipeline_behavior(logging_behavior)
    result = await mediator.send(SampleRequest("test"))
    
    assert "behavior" in called
    assert result == "Handled: test"


async def test_pipeline_behavior_short_circuit():
    """Should allow behavior to short-circuit handler."""
    mediator = Mediator()
    mediator.register_handler(SampleRequest, SampleHandler())
    
    async def short_circuit_behavior(request, handler):
        return "Short-circuited"
    
    mediator.add_pipeline_behavior(short_circuit_behavior)
    result = await mediator.send(SampleRequest("test"))
    
    assert result == "Short-circuited"
