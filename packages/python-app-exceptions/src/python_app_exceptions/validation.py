"""Validation exception classes."""

from .base import BaseApplicationException


class ValidationError(BaseApplicationException):
    """Raised when data validation fails."""

    def __init__(self, field: str, value: str = None, details: str = None):
        if value:
            message = f"validation failed for field '{field}' with value '{value}'"
        else:
            message = f"validation failed for field '{field}'"
        super().__init__(message, details)


class InvalidInputError(ValidationError):
    """Raised when input data is invalid."""

    def __init__(self, input_name: str, expected_format: str = None):
        details = f"expected format: {expected_format}" if expected_format else None
        super().__init__(input_name, details=details)






