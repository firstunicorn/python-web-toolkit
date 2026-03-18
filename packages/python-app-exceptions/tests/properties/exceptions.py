"""Generic exception property testing utilities.

This module contains utilities for testing exception handling
and string representations across different exception types.

RULE: Maximum 100 lines per file.
"""


class GenericExceptionProperties:
    """Generic property-based test patterns for exception handling."""
    
    @staticmethod
    def test_exception_string_representation(
        exception: Exception,
        should_contain_input: str = None
    ) -> None:
        """Test that exception produces valid string representations.
        
        Args:
            exception: Exception instance to test
            should_contain_input: Optional input that should be in error message
            
        Raises:
            pytest.fail: If exception string representation is invalid
        """
        try:
            # Test basic string conversion
            error_str = str(exception)
            repr_str = repr(exception)
            
            # String representation should be valid and non-empty
            assert isinstance(error_str, str), (
                f"str(exception) must return string, got {type(error_str)}"
            )
            assert isinstance(repr_str, str), (
                f"repr(exception) must return string, got {type(repr_str)}"
            )
            assert len(error_str) > 0, "Exception string representation cannot be empty"
            
            # Should include input in message if provided and non-empty
            if should_contain_input and should_contain_input.strip():
                assert should_contain_input in error_str, (
                    f"Exception message should contain input '{should_contain_input}'"
                )
                
        except Exception as e:
            raise AssertionError(f"Exception {type(exception).__name__} string conversion failed: {e}")
    
    @staticmethod
    def test_exception_instantiation_robustness(
        exception_class: type,
        input_value: str
    ) -> None:
        """Test that exception class can be instantiated with any string input.
        
        Args:
            exception_class: Exception class to test
            input_value: String input to use for exception instantiation
        """
        try:
            # Should be able to create exception with any string input
            exception_instance = exception_class(input_value)
            
            # Should be instance of expected type
            assert isinstance(exception_instance, exception_class), (
                f"Created instance should be of type {exception_class.__name__}"
            )
            
            # Should be able to convert to string
            str_repr = str(exception_instance)
            assert isinstance(str_repr, str), "Exception string conversion failed"
            assert len(str_repr) > 0, "Exception string should not be empty"
            
        except Exception as e:
            raise AssertionError(
                f"Failed to create {exception_class.__name__} with input '{input_value}': {e}"
            )
    
    @staticmethod
    def test_exception_inheritance_properties(exception: Exception) -> None:
        """Test that exception follows proper inheritance patterns.
        
        Args:
            exception: Exception instance to test
        """
        # Should inherit from Exception base class
        assert isinstance(exception, Exception), (
            f"{type(exception).__name__} should inherit from Exception"
        )
        
        # Should have proper type information
        assert hasattr(exception, '__class__'), "Exception should have __class__ attribute"
        assert hasattr(exception, '__module__'), "Exception should have __module__ attribute"