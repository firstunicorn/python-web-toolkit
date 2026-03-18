"""Unit tests for CQRS interfaces.

Tests ICommand, IQuery, ICommandHandler, IQueryHandler interfaces.
RULE: Maximum 100 lines per file.
"""

import pytest
from pydantic import BaseModel

from python_cqrs_core import ICommand, IQuery, ICommandHandler, IQueryHandler


# Test implementations (renamed from TestCommand to avoid pytest collection warnings)
class SampleCommand(BaseModel, ICommand):
    """Sample command implementation for testing."""
    name: str
    value: int


class SampleQuery(BaseModel, IQuery):
    """Sample query implementation for testing."""
    id: int


class SampleCommandHandler(ICommandHandler[SampleCommand, str]):
    """Sample command handler implementation for testing."""

    async def handle(self, command: SampleCommand) -> str:
        return f"Handled: {command.name}"


class SampleQueryHandler(IQueryHandler[SampleQuery, dict]):
    """Sample query handler implementation for testing."""

    async def handle(self, query: SampleQuery) -> dict:
        return {"id": query.id, "found": True}


class TestInterfaces:
    """Tests for CQRS interfaces."""

    def test_command_interface_can_be_implemented(self):
        """ICommand interface can be implemented with Pydantic."""
        cmd = SampleCommand(name="test", value=42)
        assert isinstance(cmd, ICommand)
        assert cmd.name == "test"
        assert cmd.value == 42

    def test_query_interface_can_be_implemented(self):
        """IQuery interface can be implemented with Pydantic."""
        query = SampleQuery(id=1)
        assert isinstance(query, IQuery)
        assert query.id == 1

    @pytest.mark.asyncio
    async def test_command_handler_interface(self):
        """ICommandHandler interface enforces handle method."""
        handler = SampleCommandHandler()
        cmd = SampleCommand(name="test", value=42)
        result = await handler.handle(cmd)
        assert result == "Handled: test"

    @pytest.mark.asyncio
    async def test_query_handler_interface(self):
        """IQueryHandler interface enforces handle method."""
        handler = SampleQueryHandler()
        query = SampleQuery(id=1)
        result = await handler.handle(query)
        assert result == {"id": 1, "found": True}

    def test_command_is_abstract_base(self):
        """ICommand is an abstract base class."""
        from abc import ABC
        assert issubclass(ICommand, ABC)

    def test_query_is_abstract_base(self):
        """IQuery is an abstract base class."""
        from abc import ABC
        assert issubclass(IQuery, ABC)

    def test_command_handler_is_abstract_base(self):
        """ICommandHandler is an abstract base class."""
        from abc import ABC
        assert issubclass(ICommandHandler, ABC)

    def test_query_handler_is_abstract_base(self):
        """IQueryHandler is an abstract base class."""
        from abc import ABC
        assert issubclass(IQueryHandler, ABC)

    def test_command_handler_has_generic_types(self):
        """ICommandHandler should support generic typing."""
        handler = SampleCommandHandler()
        assert hasattr(handler, 'handle')

    def test_query_handler_has_generic_types(self):
        """IQueryHandler should support generic typing."""
        handler = SampleQueryHandler()
        assert hasattr(handler, 'handle')
