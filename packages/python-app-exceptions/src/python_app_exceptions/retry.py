"""Retry logic exception classes."""

from .base import BaseApplicationException


class RetryExhaustedException(BaseApplicationException):
    """Raised when retry attempts are exhausted."""

    def __init__(self, operation: str, attempts: int):
        message = f"retry exhausted for operation '{operation}' after {attempts} attempts"
        super().__init__(message)


class RetryableError(BaseApplicationException):
    """Raised for errors that can be retried."""

    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after






