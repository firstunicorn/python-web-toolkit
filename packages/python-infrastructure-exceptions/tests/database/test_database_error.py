"""Unit tests for DatabaseError.

Tests database-related infrastructure exceptions.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import DatabaseError, InfrastructureException


class TestDatabaseError:
    """Tests for DatabaseError."""

    def test_database_error_basic(self):
        """DatabaseError should accept message."""
        exc = DatabaseError("Connection pool exhausted")
        assert "Connection pool exhausted" in str(exc)

    def test_database_error_with_query(self):
        """DatabaseError should accept optional query parameter."""
        exc = DatabaseError("Query timeout", query="SELECT * FROM users")
        assert exc.query == "SELECT * FROM users"

    def test_database_error_inheritance(self):
        """DatabaseError should inherit from InfrastructureException."""
        exc = DatabaseError("test")
        assert isinstance(exc, InfrastructureException)
