"""Configuration infrastructure exceptions."""

from .base import InfrastructureException


class ConfigurationError(InfrastructureException):
    """
    Configuration infrastructure error.

    Use for:
    - Missing environment variables
    - Invalid configuration values
    - Configuration file not found
    - Secret not found
    - Invalid credentials

    Examples:
        raise ConfigurationError("Missing DATABASE_URL environment variable")
        raise ConfigurationError("Invalid log level", details="Expected: DEBUG, INFO, WARNING, ERROR")
        raise ConfigurationError("Config file not found", details="config.yaml not found in /etc/app/")
    """

    def __init__(self, message: str, details: str = None, config_key: str = None):
        """
        Initialize configuration error.

        Args:
            message: Human-readable error message
            details: Optional technical details
            config_key: Optional configuration key that caused the error
        """
        self.config_key = config_key
        super().__init__(message, details)

