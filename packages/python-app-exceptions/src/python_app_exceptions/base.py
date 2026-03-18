"""Base exception classes for Python web applications."""


class BaseApplicationException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: str = None):
        self.message = message or "No message provided"
        self.details = details
        if details:
            full_message = f"{self.message}: {details}"
        else:
            full_message = self.message
        super().__init__(full_message)






