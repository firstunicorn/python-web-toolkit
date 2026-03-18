"""Base infrastructure exception class."""


class InfrastructureException(Exception):
    """
    Base exception for all infrastructure-layer errors.

    Infrastructure errors are low-level technical failures:
    - Database connection/query failures
    - External API timeouts
    - Cache unavailability
    - Message queue failures
    - Configuration issues

    These are distinct from business/application layer errors
    (validation, business rules) which use python-app-exceptions.
    """

    def __init__(self, message: str, details: str = None):
        """
        Initialize infrastructure exception.

        Args:
            message: Human-readable error message
            details: Optional technical details for debugging
        """
        self.message = message
        self.details = details

        if details:
            full_message = f"{message}: {details}"
        else:
            full_message = message

        super().__init__(full_message)

