"""Unit tests for ConfigurationError.

Tests configuration-related infrastructure exceptions.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import ConfigurationError


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error_basic(self):
        """ConfigurationError should accept message."""
        exc = ConfigurationError("Missing DATABASE_URL")
        assert "Missing DATABASE_URL" in str(exc)

    def test_configuration_error_with_config_key(self):
        """ConfigurationError should accept config_key."""
        exc = ConfigurationError("Invalid value", config_key="LOG_LEVEL")
        assert exc.config_key == "LOG_LEVEL"
