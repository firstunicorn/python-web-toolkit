"""External service infrastructure exceptions."""

from .base import InfrastructureException


class ExternalServiceError(InfrastructureException):
    """
    External service/API infrastructure error.

    Use for:
    - Third-party API timeouts
    - HTTP request failures
    - OAuth/authentication failures
    - Rate limiting
    - Service unavailable

    Examples:
        raise ExternalServiceError("Stripe API timeout", service_name="stripe")
        raise ExternalServiceError("SendGrid rate limit", service_name="sendgrid", details="429 Too Many Requests")
        raise ExternalServiceError("OAuth token expired", service_name="google")
    """

    def __init__(
        self,
        message: str,
        service_name: str = None,
        details: str = None,
        status_code: int = None
    ):
        """
        Initialize external service error.

        Args:
            message: Human-readable error message
            service_name: Name of the external service (e.g., "stripe", "sendgrid")
            details: Optional technical details
            status_code: Optional HTTP status code
        """
        self.service_name = service_name
        self.status_code = status_code
        super().__init__(message, details)

