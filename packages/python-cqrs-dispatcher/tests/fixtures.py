"""Shared test fixtures for CQRS dispatcher tests.

RULE: Maximum 100 lines per file.
"""

from python_cqrs_core import ICommand, IQuery, ICommandHandler, IQueryHandler
from typing import Any


# Test command and handler
class SampleCommand(ICommand):
    """Sample command for testing."""
    def __init__(self, value: str):
        self.value = value


class SampleCommandHandler(ICommandHandler):
    """Sample command handler for testing."""
    async def handle(self, command: SampleCommand) -> str:
        return f"Command: {command.value}"


# Test query and handler
class SampleQuery(IQuery):
    """Sample query for testing."""
    def __init__(self, query_id: int):
        self.query_id = query_id


class SampleQueryHandler(IQueryHandler):
    """Sample query handler for testing."""
    async def handle(self, query: SampleQuery) -> dict:
        return {"id": query.query_id, "data": "test"}


# Additional command for testing
class AnotherCommand(ICommand):
    """Another test command."""
    def __init__(self, data: str):
        self.data = data


class AnotherCommandHandler(ICommandHandler):
    """Another test command handler."""
    async def handle(self, command: AnotherCommand) -> bool:
        return True
