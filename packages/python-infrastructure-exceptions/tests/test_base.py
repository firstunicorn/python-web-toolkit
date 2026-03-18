"""Unit tests for base InfrastructureException.

Tests the base infrastructure exception class.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import InfrastructureException


class TestInfrastructureException:
    """Tests for base InfrastructureException."""

    def test_base_exception_with_message(self):
        """InfrastructureException should accept message."""
        exc = InfrastructureException("Infrastructure failure")
        assert exc.message == "Infrastructure failure"
        assert "Infrastructure failure" in str(exc)

    def test_base_exception_with_details(self):
        """InfrastructureException should accept details."""
        exc = InfrastructureException("Failure", details="Connection timeout")
        assert exc.details == "Connection timeout"
        assert "Connection timeout" in str(exc)

    def test_base_exception_inheritance(self):
        """InfrastructureException should inherit from Exception."""
        exc = InfrastructureException("test")
        assert isinstance(exc, Exception)
