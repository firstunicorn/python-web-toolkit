"""Business logic exception classes."""

from .base import BaseApplicationException


class BusinessLogicError(BaseApplicationException):
    """Raised when business rules are violated."""

    def __init__(self, rule: str, details: str = None):
        message = f"business rule violation: {rule}"
        super().__init__(message, details)






