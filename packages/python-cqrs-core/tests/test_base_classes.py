"""Unit tests for CQRS base classes.

Tests BaseCommand, BaseQuery, PaginatedQuery with tracing fields.
RULE: Maximum 100 lines per file.
"""

import pytest
from uuid import UUID
from datetime import datetime, timezone

from python_cqrs_core import BaseCommand, BaseQuery, PaginatedQuery


class CreateUserCommand(BaseCommand):
    """Test command extending BaseCommand."""
    name: str
    email: str


class GetUserQuery(BaseQuery):
    """Test query extending BaseQuery."""
    user_id: int


class ListUsersQuery(PaginatedQuery):
    """Test paginated query extending PaginatedQuery."""
    status: str = "active"


class TestBaseCommand:
    """Tests for BaseCommand class."""

    def test_base_command_auto_generates_request_id(self):
        """BaseCommand should auto-generate request_id."""
        cmd = CreateUserCommand(name="John", email="john@test.com")
        assert isinstance(cmd.request_id, UUID)

    def test_base_command_auto_generates_requested_at(self):
        """BaseCommand should auto-generate requested_at timestamp."""
        cmd = CreateUserCommand(name="John", email="john@test.com")
        assert isinstance(cmd.requested_at, datetime)
        assert cmd.requested_at.tzinfo == timezone.utc

    def test_base_command_accepts_correlation_id(self):
        """BaseCommand should accept optional correlation_id."""
        from uuid import uuid4
        correlation_id = uuid4()
        cmd = CreateUserCommand(
            name="John",
            email="john@test.com",
            correlation_id=correlation_id
        )
        assert cmd.correlation_id == correlation_id

    def test_base_command_accepts_requested_by(self):
        """BaseCommand should accept optional requested_by."""
        cmd = CreateUserCommand(
            name="John",
            email="john@test.com",
            requested_by="admin"
        )
        assert cmd.requested_by == "admin"

    def test_base_command_is_frozen(self):
        """BaseCommand instances should be immutable."""
        cmd = CreateUserCommand(name="John", email="john@test.com")
        with pytest.raises(Exception):  # Pydantic raises ValidationError
            cmd.name = "Jane"


class TestBaseQuery:
    """Tests for BaseQuery class."""

    def test_base_query_auto_generates_request_id(self):
        """BaseQuery should auto-generate request_id."""
        query = GetUserQuery(user_id=1)
        assert isinstance(query.request_id, UUID)

    def test_base_query_is_frozen(self):
        """BaseQuery instances should be immutable."""
        query = GetUserQuery(user_id=1)
        with pytest.raises(Exception):
            query.user_id = 2


class TestPaginatedQuery:
    """Tests for PaginatedQuery class."""

    def test_paginated_query_defaults(self):
        """PaginatedQuery should have sensible defaults."""
        query = ListUsersQuery()
        assert query.page == 1
        assert query.page_size == 10

    def test_paginated_query_calculates_offset(self):
        """PaginatedQuery should calculate offset correctly."""
        query = ListUsersQuery(page=3, page_size=20)
        assert query.offset == 40  # (3 - 1) * 20

    def test_paginated_query_page_1_offset_0(self):
        """Page 1 should have offset 0."""
        query = ListUsersQuery(page=1, page_size=10)
        assert query.offset == 0
