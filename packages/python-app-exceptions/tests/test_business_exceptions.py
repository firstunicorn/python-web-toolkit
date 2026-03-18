"""Property-based tests for business logic exceptions.

Tests BusinessLogicError with various inputs.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, settings, strategies as st

from python_app_exceptions import BusinessLogicError
from .strategies.text import any_text_input_strategy, safe_ascii_text_strategy
from .mixins.exceptions import ExceptionTestMixin


class TestBusinessLogicError(ExceptionTestMixin):
    """Property-based tests for BusinessLogicError."""

    @given(rule=any_text_input_strategy())
    @settings(deadline=None)
    def test_handles_any_rule_input(self, rule):
        """BusinessLogicError should handle any rule input."""
        exception = BusinessLogicError(rule)
        self.validate_exception_properties(exception)

    @given(
        rule=safe_ascii_text_strategy(),
        details=safe_ascii_text_strategy()
    )
    def test_handles_rule_and_details(self, rule, details):
        """BusinessLogicError should handle rule and details."""
        exception = BusinessLogicError(rule, details)
        
        # Validate basic properties
        self.validate_exception_properties(exception)
        
        # Should contain "business rule violation" in message
        exception_str = str(exception)
        assert "business rule violation" in exception_str.lower()
        
        # Should contain rule if non-empty
        if rule.strip():
            assert rule in exception_str
        
        # Should contain details if provided
        if details and details.strip():
            assert details in exception_str

    def test_exception_formats_message_correctly(self):
        """BusinessLogicError should format message with 'business rule violation'."""
        exception = BusinessLogicError("user must be admin")
        assert "business rule violation: user must be admin" in str(exception)

    def test_exception_with_details(self):
        """BusinessLogicError with details should include both rule and details."""
        exception = BusinessLogicError("payment required", "balance insufficient")
        exception_str = str(exception)
        assert "business rule violation: payment required" in exception_str
        assert "balance insufficient" in exception_str

    def test_exception_without_details(self):
        """BusinessLogicError without details should work correctly."""
        exception = BusinessLogicError("age restriction")
        assert "business rule violation: age restriction" in str(exception)

    @given(rule=any_text_input_strategy())
    def test_exception_instantiation_robustness(self, rule):
        """BusinessLogicError can be instantiated with any rule text."""
        self.validate_exception_instantiation(BusinessLogicError, rule)

    def test_exception_inheritance(self):
        """BusinessLogicError should inherit from BaseApplicationException."""
        from python_app_exceptions import BaseApplicationException
        exception = BusinessLogicError("test")
        assert isinstance(exception, BaseApplicationException)
        assert isinstance(exception, Exception)

    @given(
        rule=st.text(min_size=1, max_size=50),
        details=st.one_of(st.none(), st.text(min_size=1, max_size=50))
    )
    def test_exception_can_be_raised_and_caught(self, rule, details):
        """BusinessLogicError can be raised and caught properly."""
        with pytest.raises(BusinessLogicError) as exc_info:
            raise BusinessLogicError(rule, details)
        
        assert "business rule violation" in str(exc_info.value).lower()
