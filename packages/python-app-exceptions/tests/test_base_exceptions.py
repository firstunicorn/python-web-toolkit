"""Property-based tests for base exception classes.

Tests BaseApplicationException with various inputs to ensure robustness.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_app_exceptions import BaseApplicationException
from .strategies.text import any_text_input_strategy, safe_ascii_text_strategy
from .properties.exceptions import GenericExceptionProperties
from .mixins.exceptions import ExceptionTestMixin


class TestBaseApplicationException(ExceptionTestMixin):
    """Property-based tests for BaseApplicationException."""

    @given(message=any_text_input_strategy())
    def test_handles_any_message_input(self, message):
        """BaseApplicationException should handle any message input."""
        exception = BaseApplicationException(message)
        self.validate_exception_properties(exception, message if message else None)

    @given(
        message=safe_ascii_text_strategy(),
        details=safe_ascii_text_strategy()
    )
    def test_handles_message_and_details(self, message, details):
        """BaseApplicationException should handle message and details."""
        exception = BaseApplicationException(message, details)

        # Validate basic exception properties
        self.validate_exception_properties(exception)

        # Should contain message in string representation
        exception_str = str(exception)
        if message.strip():
            assert message in exception_str

        # Should contain details if provided
        if details and details.strip():
            assert details in exception_str

    def test_exception_without_details(self):
        """BaseApplicationException without details should work correctly."""
        exception = BaseApplicationException("Test error")
        assert str(exception) == "Test error"
        assert exception.message == "Test error"
        assert exception.details is None

    def test_exception_with_details(self):
        """BaseApplicationException with details should format correctly."""
        exception = BaseApplicationException("Test error", "Additional info")
        assert "Test error: Additional info" in str(exception)
        assert exception.message == "Test error"
        assert exception.details == "Additional info"

    def test_exception_with_empty_details(self):
        """BaseApplicationException with empty details should ignore them."""
        exception = BaseApplicationException("Test error", "")
        assert str(exception) == "Test error"

    @given(text=any_text_input_strategy())
    def test_exception_instantiation_robustness(self, text):
        """BaseApplicationException can be instantiated with any text."""
        self.validate_exception_instantiation(BaseApplicationException, text)

    def test_exception_inheritance(self):
        """BaseApplicationException should inherit from Exception."""
        exception = BaseApplicationException("test")
        self.validate_exception_inheritance(exception)
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        """BaseApplicationException should have expected attributes."""
        exception = BaseApplicationException("test", "details")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'details')
        assert exception.message == "test"
        assert exception.details == "details"

    @given(
        message=st.text(min_size=1, max_size=50),
        details=st.one_of(st.none(), st.text(min_size=1, max_size=50))
    )
    def test_exception_can_be_raised_and_caught(self, message, details):
        """BaseApplicationException can be raised and caught properly."""
        with pytest.raises(BaseApplicationException) as exc_info:
            raise BaseApplicationException(message, details)

        assert exc_info.value.message == message
        assert exc_info.value.details == details
