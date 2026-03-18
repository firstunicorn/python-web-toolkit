"""Preset configurations for different environments.

Per PRD specifications
"""

from typing import Optional
from python_structlog_config.config import configure_structlog


def configure_for_development(service_name: str) -> None:
    """Development preset - console output, debug level.
    
    Args:
        service_name: Service name for context
    
    Example:
        >>> configure_for_development("my-api")
    """
    configure_structlog(
        log_level="DEBUG",
        json_output=False,
        enable_otel=False,
        enable_sentry=False,
        service_name=service_name
    )


def configure_for_production(
    service_name: str,
    sentry_dsn: Optional[str] = None,
    log_level: str = "INFO"
) -> None:
    """Production preset - JSON output, OTel, optional Sentry.
    
    Args:
        service_name: Service name for context
        sentry_dsn: Sentry DSN (optional)
        log_level: Logging level (default: INFO)
    
    Example:
        >>> configure_for_production(
        ...     "my-api",
        ...     sentry_dsn="https://...@sentry.io/..."
        ... )
    """
    configure_structlog(
        log_level=log_level,
        json_output=True,
        enable_otel=True,
        enable_sentry=bool(sentry_dsn),
        sentry_dsn=sentry_dsn,
        service_name=service_name,
        environment="production"
    )


def configure_for_testing(service_name: str) -> None:
    """Testing preset - minimal output, warning level.
    
    Args:
        service_name: Service name for context
    
    Example:
        >>> configure_for_testing("my-api")
    """
    configure_structlog(
        log_level="WARNING",
        json_output=False,
        enable_otel=False,
        enable_sentry=False,
        service_name=service_name
    )
