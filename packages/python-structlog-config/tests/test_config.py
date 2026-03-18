"""Tests for structlog configuration."""

import pytest
import structlog
from python_structlog_config import (
    configure_structlog,
    get_logger,
    configure_for_development,
    configure_for_production,
    configure_for_testing
)


def test_configure_structlog_json():
    """Test JSON output configuration."""
    configure_structlog(json_output=True)
    logger = get_logger()
    
    assert logger is not None


def test_configure_structlog_console():
    """Test console output configuration."""
    configure_structlog(json_output=False)
    logger = get_logger()
    
    assert logger is not None


def test_get_logger():
    """Test logger retrieval."""
    configure_structlog()
    logger = get_logger(__name__)
    
    assert logger is not None


def test_configure_for_development():
    """Test development preset."""
    configure_for_development("test-api")
    logger = get_logger()
    
    assert logger is not None


def test_configure_for_production():
    """Test production preset without Sentry."""
    configure_for_production("test-api")
    logger = get_logger()
    
    assert logger is not None


def test_configure_for_testing():
    """Test testing preset."""
    configure_for_testing("test-api")
    logger = get_logger()
    
    assert logger is not None


def test_logger_info():
    """Test basic logging."""
    configure_structlog()
    logger = get_logger()
    
    # Should not raise
    logger.info("test message", key="value")
