"""Unit tests for CQRSDispatcher.

Tests the main dispatcher class functionality.
RULE: Maximum 100 lines per file.
"""

import pytest
from python_cqrs_dispatcher import CQRSDispatcher
from tests.fixtures import (
    SampleCommand, SampleCommandHandler,
    SampleQuery, SampleQueryHandler,
    AnotherCommand
)


class TestCQRSDispatcherRegistration:
    """Tests for handler registration."""

    def test_register_command_handler(self):
        """Should register command handler successfully."""
        dispatcher = CQRSDispatcher()
        handler = SampleCommandHandler()
        
        dispatcher.register_command_handler(SampleCommand, handler)
        assert SampleCommand in dispatcher._command_handlers

    def test_register_duplicate_command_raises(self):
        """Should raise on duplicate command registration."""
        dispatcher = CQRSDispatcher()
        handler = SampleCommandHandler()
        
        dispatcher.register_command_handler(SampleCommand, handler)
        with pytest.raises(ValueError, match="Handler already registered"):
            dispatcher.register_command_handler(SampleCommand, handler)

    def test_register_query_handler(self):
        """Should register query handler successfully."""
        dispatcher = CQRSDispatcher()
        handler = SampleQueryHandler()
        
        dispatcher.register_query_handler(SampleQuery, handler)
        assert SampleQuery in dispatcher._query_handlers

    def test_register_duplicate_query_raises(self):
        """Should raise on duplicate query registration."""
        dispatcher = CQRSDispatcher()
        handler = SampleQueryHandler()
        
        dispatcher.register_query_handler(SampleQuery, handler)
        with pytest.raises(ValueError, match="Handler already registered"):
            dispatcher.register_query_handler(SampleQuery, handler)


class TestCQRSDispatcherExecution:
    """Tests for command/query execution."""

    async def test_send_command(self):
        """Should execute command successfully."""
        dispatcher = CQRSDispatcher()
        dispatcher.register_command_handler(SampleCommand, SampleCommandHandler())
        
        result = await dispatcher.send_command(SampleCommand("test"))
        assert result == "Command: test"

    async def test_send_command_unregistered_raises(self):
        """Should raise on unregistered command."""
        dispatcher = CQRSDispatcher()
        
        with pytest.raises(ValueError, match="No handler for command"):
            await dispatcher.send_command(AnotherCommand("test"))

    async def test_send_query(self):
        """Should execute query successfully."""
        dispatcher = CQRSDispatcher()
        dispatcher.register_query_handler(SampleQuery, SampleQueryHandler())
        
        result = await dispatcher.send_query(SampleQuery(42))
        assert result == {"id": 42, "data": "test"}

    async def test_send_query_unregistered_raises(self):
        """Should raise on unregistered query."""
        dispatcher = CQRSDispatcher()
        query = SampleQuery(1)
        
        with pytest.raises(ValueError, match="No handler for query"):
            await dispatcher.send_query(query)


class TestPipelineBehavior:
    """Tests for pipeline behavior integration."""

    async def test_add_pipeline_behavior(self):
        """Should integrate with mediator pipeline."""
        dispatcher = CQRSDispatcher()
        dispatcher.register_command_handler(SampleCommand, SampleCommandHandler())
        
        # Simple logging behavior
        called = []
        async def log_behavior(request, handler):
            called.append(type(request).__name__)
            return None  # Return None to let mediator execute handler
        
        dispatcher.add_pipeline_behavior(log_behavior)
        result = await dispatcher.send_command(SampleCommand("test"))
        
        assert "SampleCommand" in called
        assert result == "Command: test"
