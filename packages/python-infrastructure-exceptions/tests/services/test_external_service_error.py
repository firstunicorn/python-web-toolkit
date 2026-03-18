"""Unit tests for ExternalServiceError.

Tests external service integration errors.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import ExternalServiceError


class TestExternalServiceError:
    """Tests for ExternalServiceError."""

    def test_external_service_error_basic(self):
        """ExternalServiceError should accept message."""
        exc = ExternalServiceError("Stripe API timeout")
        assert "Stripe API timeout" in str(exc)

    def test_external_service_error_with_service_name(self):
        """ExternalServiceError should accept service_name."""
        exc = ExternalServiceError("API timeout", service_name="stripe")
        assert exc.service_name == "stripe"

    def test_external_service_error_with_status_code(self):
        """ExternalServiceError should accept status_code."""
        exc = ExternalServiceError("Rate limit", service_name="sendgrid", status_code=429)
        assert exc.status_code == 429
