"""Optional integrations for OTel and Sentry.

Per PRD specifications
"""

from typing import Optional
import structlog


def setup_otel_logging(service_name: Optional[str] = None) -> None:
    """Setup OpenTelemetry logging integration.
    
    Args:
        service_name: Service name for context
    
    Example:
        >>> setup_otel_logging("my-api")
    """
    try:
        from opentelemetry.instrumentation.logging import (
            LoggingInstrumentor
        )
        
        # Instrument logging with OTel
        LoggingInstrumentor().instrument(set_logging_format=True)
        
        # Bind service name to context if provided
        if service_name:
            structlog.contextvars.bind_contextvars(service=service_name)
        
    except ImportError:
        logger = structlog.get_logger()
        logger.warning(
            "OpenTelemetry logging not available",
            hint="Install: pip install opentelemetry-instrumentation-logging"
        )


def setup_sentry_logging(
    sentry_dsn: str,
    environment: Optional[str] = None
) -> None:
    """Setup Sentry logging integration.
    
    Args:
        sentry_dsn: Sentry DSN
        environment: Environment name (dev, staging, prod)
    
    Example:
        >>> setup_sentry_logging(
        ...     "https://...@sentry.io/...",
        ...     environment="production"
        ... )
    """
    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        # Initialize Sentry with logging integration
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment or "production",
            integrations=[
                LoggingIntegration(
                    level=None,  # Capture all levels
                    event_level=None  # Send as breadcrumbs
                )
            ],
        )
        
    except ImportError:
        logger = structlog.get_logger()
        logger.warning(
            "Sentry SDK not available",
            hint="Install: pip install sentry-sdk"
        )
