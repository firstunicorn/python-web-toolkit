"""Core structlog configuration.

Extracted from GridFlow backend/src/infrastructure/logging_config.py
Enhanced with OTel and Sentry support per PRD specifications
"""

import structlog
from typing import Optional


def configure_structlog(
    log_level: str = "INFO",
    json_output: bool = False,
    enable_otel: bool = False,
    enable_sentry: bool = False,
    sentry_dsn: Optional[str] = None,
    service_name: Optional[str] = None,
    environment: Optional[str] = None
) -> None:
    """Configure structlog with optional OTel and Sentry integration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: Use JSON renderer instead of console (default: False)
        enable_otel: Enable OpenTelemetry integration (default: False)
        enable_sentry: Enable Sentry integration (default: False)
        sentry_dsn: Sentry DSN (required if enable_sentry=True)
        service_name: Service name for context (optional)
        environment: Environment name (dev, staging, prod)
    
    Example:
        >>> configure_structlog(
        ...     log_level="INFO",
        ...     json_output=True,
        ...     service_name="my-api"
        ... )
    """
    # Build processor chain
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add OTel integration if enabled
    if enable_otel:
        from python_structlog_config.integrations import setup_otel_logging
        setup_otel_logging(service_name)
    
    # Add Sentry integration if enabled
    if enable_sentry and sentry_dsn:
        from python_structlog_config.integrations import setup_sentry_logging
        setup_sentry_logging(sentry_dsn, environment)
    
    # Choose renderer based on output format
    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None):
    """Get a structlog logger instance.
    
    Args:
        name: Logger name (optional)
    
    Returns:
        Structlog logger instance
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return structlog.get_logger(name)
