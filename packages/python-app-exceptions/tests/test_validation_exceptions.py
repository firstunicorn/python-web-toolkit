"""Property-based tests for validation exceptions.

Tests ValidationError and InvalidInputError with various inputs.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_app_exceptions import ValidationError, InvalidInputError
from .strategies.text import any_text_input_strategy, safe_ascii_text_strategy
from .mixins.exceptions import ExceptionTestMixin


class TestValidationError(ExceptionTestMixin):
    """Property-based tests for ValidationError."""

    @given(field=any_text_input_strategy())
    def test_handles_any_field_input(self, field):
        """ValidationError should handle any field input."""
        exception = ValidationError(field)
        self.validate_exception_properties(exception)

    @given(
        field=safe_ascii_text_strategy(),
        value=safe_ascii_text_strategy(),
        details=safe_ascii_text_strategy()
    )
    def test_handles_field_value_and_details(self, field, value, details):
        """ValidationError should handle field, value, and details."""
        exception = ValidationError(field, value, details)
        
        self.validate_exception_properties(exception)
        exception_str = str(exception)
        
        # Should contain "validation failed"
        assert "validation failed" in exception_str.lower()
        
        # Should contain field if non-empty
        if field.strip():
            assert field in exception_str

    def test_exception_with_field_only(self):
        """ValidationError with field only should format correctly."""
        exception = ValidationError("email")
        assert "validation failed for field 'email'" in str(exception)

    def test_exception_with_field_and_value(self):
        """ValidationError with field and value should format correctly."""
        exception = ValidationError("email", "invalid@")
        exception_str = str(exception)
        assert "validation failed for field 'email'" in exception_str
        assert "invalid@" in exception_str

    def test_exception_with_all_params(self):
        """ValidationError with all params should include everything."""
        exception = ValidationError("email", "bad", "must be valid email")
        exception_str = str(exception)
        assert "email" in exception_str
        assert "bad" in exception_str
        assert "must be valid email" in exception_str

    @given(field=st.text(min_size=1, max_size=30))
    def test_exception_can_be_raised(self, field):
        """ValidationError can be raised and caught."""
        with pytest.raises(ValidationError):
            raise ValidationError(field)


class TestInvalidInputError(ExceptionTestMixin):
    """Property-based tests for InvalidInputError."""

    @given(input_name=any_text_input_strategy())
    def test_handles_any_input_name(self, input_name):
        """InvalidInputError should handle any input_name."""
        exception = InvalidInputError(input_name)
        self.validate_exception_properties(exception)

    @given(
        input_name=safe_ascii_text_strategy(),
        expected_format=safe_ascii_text_strategy()
    )
    def test_handles_input_name_and_format(self, input_name, expected_format):
        """InvalidInputError should handle input_name and expected_format."""
        exception = InvalidInputError(input_name, expected_format)
        self.validate_exception_properties(exception)

    def test_exception_with_expected_format(self):
        """InvalidInputError with expected_format should include it."""
        exception = InvalidInputError("phone", "E.164 format")
        exception_str = str(exception)
        assert "expected format: E.164 format" in exception_str

    def test_exception_inherits_from_validation_error(self):
        """InvalidInputError should inherit from ValidationError."""
        exception = InvalidInputError("test")
        assert isinstance(exception, ValidationError)
