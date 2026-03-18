"""Python Structlog Config - Structured logging configuration."""

from python_structlog_config.config import configure_structlog, get_logger
from python_structlog_config.presets import (
    configure_for_development,
    configure_for_production,
    configure_for_testing
)

__version__ = "0.1.0"

__all__ = [
    "configure_structlog",
    "get_logger",
    "configure_for_development",
    "configure_for_production",
    "configure_for_testing",
]
