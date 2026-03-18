"""Property-based tests for retry exceptions.

Tests RetryExhaustedException and RetryableError with various inputs.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_app_exceptions import RetryExhaustedException, RetryableError
from .strategies.text import any_text_input_strategy, safe_ascii_text_strategy
from .mixins.exceptions import ExceptionTestMixin


class TestRetryExhaustedException(ExceptionTestMixin):
    """Property-based tests for RetryExhaustedException."""

    @given(
        operation=any_text_input_strategy(),
        attempts=st.integers(min_value=1, max_value=100)
    )
    def test_handles_any_operation_and_attempts(self, operation, attempts):
        """RetryExhaustedException should handle any operation and attempts."""
        exception = RetryExhaustedException(operation, attempts)
        self.validate_exception_properties(exception)

        exception_str = str(exception)
        assert "retry exhausted" in exception_str.lower()
        assert str(attempts) in exception_str

    def test_exception_formats_message_correctly(self):
        """RetryExhaustedException should format message with operation and attempts."""
        exception = RetryExhaustedException("database_query", 5)
        exception_str = str(exception)
        assert "retry exhausted" in exception_str.lower()
        assert "database_query" in exception_str
        assert "5" in exception_str
        assert "attempts" in exception_str.lower()

    @given(
        operation=safe_ascii_text_strategy(),
        attempts=st.integers(min_value=0, max_value=1000)
    )
    def test_exception_can_be_raised(self, operation, attempts):
        """RetryExhaustedException can be raised and caught."""
        with pytest.raises(RetryExhaustedException) as exc_info:
            raise RetryExhaustedException(operation, attempts)

        assert "retry exhausted" in str(exc_info.value).lower()

    def test_exception_inheritance(self):
        """RetryExhaustedException should inherit from BaseApplicationException."""
        from python_app_exceptions import BaseApplicationException
        exception = RetryExhaustedException("test", 3)
        assert isinstance(exception, BaseApplicationException)


class TestRetryableError(ExceptionTestMixin):
    """Property-based tests for RetryableError."""

    @given(message=any_text_input_strategy())
    def test_handles_any_message(self, message):
        """RetryableError should handle any message input."""
        exception = RetryableError(message)
        self.validate_exception_properties(exception)

    @given(
        message=safe_ascii_text_strategy(),
        retry_after=st.one_of(st.none(), st.integers(min_value=1, max_value=3600))
    )
    def test_handles_message_and_retry_after(self, message, retry_after):
        """RetryableError should handle message and retry_after."""
        exception = RetryableError(message, retry_after)
        self.validate_exception_properties(exception)
        assert exception.retry_after == retry_after

    def test_exception_with_retry_after(self):
        """RetryableError with retry_after should store it."""
        exception = RetryableError("Rate limit exceeded", 60)
        assert exception.retry_after == 60

    def test_exception_without_retry_after(self):
        """RetryableError without retry_after should have None."""
        exception = RetryableError("Temporary failure")
        assert exception.retry_after is None

    def test_exception_inheritance(self):
        """RetryableError should inherit from BaseApplicationException."""
        from python_app_exceptions import BaseApplicationException
        exception = RetryableError("test")
        assert isinstance(exception, BaseApplicationException)

    @given(
        message=st.text(min_size=1, max_size=50),
        retry_after=st.one_of(st.none(), st.integers(min_value=1, max_value=100))
    )
    def test_exception_can_be_raised(self, message, retry_after):
        """RetryableError can be raised and caught with retry_after."""
        with pytest.raises(RetryableError) as exc_info:
            raise RetryableError(message, retry_after)

        assert exc_info.value.retry_after == retry_after
