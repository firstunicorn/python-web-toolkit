"""Unit tests for handler registry functions.

Tests bulk and auto registration helpers.
RULE: Maximum 100 lines per file.
"""

import pytest
from python_cqrs_dispatcher import CQRSDispatcher, register_handlers
from tests.fixtures import (
    SampleCommand, SampleCommandHandler,
    SampleQuery, SampleQueryHandler
)


class TestRegisterHandlers:
    """Tests for bulk handler registration."""

    def test_register_mixed_handlers(self):
        """Should register both commands and queries."""
        dispatcher = CQRSDispatcher()
        handlers = [
            (SampleCommand, SampleCommandHandler()),
            (SampleQuery, SampleQueryHandler()),
        ]
        
        register_handlers(dispatcher, handlers)
        
        assert SampleCommand in dispatcher._command_handlers
        assert SampleQuery in dispatcher._query_handlers

    def test_register_empty_list(self):
        """Should handle empty handlers list."""
        dispatcher = CQRSDispatcher()
        register_handlers(dispatcher, [])
        
        assert len(dispatcher._command_handlers) == 0
        assert len(dispatcher._query_handlers) == 0

    def test_register_invalid_type_raises(self):
        """Should raise on invalid request type."""
        dispatcher = CQRSDispatcher()
        
        class InvalidRequest:
            pass
        
        class InvalidHandler:
            async def handle(self, request):
                pass
        
        with pytest.raises(ValueError, match="Unknown request type"):
            register_handlers(dispatcher, [
                (InvalidRequest, InvalidHandler())
            ])

    async def test_registered_handlers_work(self):
        """Should execute registered handlers correctly."""
        dispatcher = CQRSDispatcher()
        handlers = [
            (SampleCommand, SampleCommandHandler()),
            (SampleQuery, SampleQueryHandler()),
        ]
        
        register_handlers(dispatcher, handlers)
        
        cmd_result = await dispatcher.send_command(SampleCommand("bulk"))
        assert cmd_result == "Command: bulk"
        
        query_result = await dispatcher.send_query(SampleQuery(99))
        assert query_result == {"id": 99, "data": "test"}
