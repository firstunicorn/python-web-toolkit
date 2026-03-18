"""Exception testing mixin for common exception testing patterns.

This mixin provides common exception testing patterns that can be
inherited by test classes to reduce code duplication.

RULE: Maximum 100 lines per file.
"""

# Conditional imports for testing dependencies
try:
    from hypothesis import given
    from ..strategies.text import any_text_input_strategy
except ImportError:
    # Fallback for when hypothesis is not available
    def given(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def any_text_input_strategy():
        return "test"

from ..properties.exceptions import GenericExceptionProperties


class ExceptionTestMixin:
    """Mixin providing common exception testing patterns."""
    
    def validate_exception_properties(self, exception: Exception, input_text: str = None):
        """Validate that exception has proper string representation.
        
        Args:
            exception: Exception instance to validate
            input_text: Optional input text that should be in exception message
            
        Uses shared exception properties to ensure consistent validation.
        """
        GenericExceptionProperties.test_exception_string_representation(
            exception, input_text
        )
    
    # Note: Removed template method test_exception_handles_any_details_input
    # Test classes should implement their own specific exception handling tests
    # rather than relying on an abstract template that gets discovered by pytest
    
    def validate_exception_inheritance(self, exception: Exception):
        """Validate that exception follows proper inheritance patterns.
        
        Args:
            exception: Exception instance to validate
        """
        GenericExceptionProperties.test_exception_inheritance_properties(exception)
    
    def validate_exception_instantiation(self, exception_class: type, input_value: str):
        """Validate that exception class can be instantiated robustly.
        
        Args:
            exception_class: Exception class to test
            input_value: Input value to use for instantiation
        """
        GenericExceptionProperties.test_exception_instantiation_robustness(
            exception_class, input_value
        )
    
    def validate_multiple_exceptions_string_representation(self, exceptions: list):
        """Validate string representation for multiple exception instances.
        
        Args:
            exceptions: List of exception instances to validate
            
        Useful for testing multiple related exception types at once.
        """
        for exception in exceptions:
            try:
                self.validate_exception_properties(exception)
            except Exception as e:
                raise AssertionError(
                    f"Exception {type(exception).__name__} validation failed: {e}"
                )
    
    def validate_exception_message_contains_details(
        self, 
        exception: Exception, 
        expected_details: list[str]
    ):
        """Validate that exception message contains expected details.
        
        Args:
            exception: Exception instance to validate
            expected_details: List of strings that should be in exception message
        """
        exception_str = str(exception)
        
        for detail in expected_details:
            if detail and detail.strip():  # Only check non-empty details
                assert detail in exception_str, (
                    f"Exception message should contain '{detail}', "
                    f"got: {exception_str}"
                )
