"""Unit tests for OutboxConfig.

Tests configuration validation and defaults.
RULE: Maximum 100 lines per file.
"""

import pytest
from pydantic import ValidationError
from python_outbox_core import OutboxConfig


def test_config_defaults():
    """Should use sensible defaults."""
    config = OutboxConfig()
    
    assert config.batch_size == 100
    assert config.poll_interval_seconds == 5
    assert config.max_retry_count == 3
    assert config.retry_backoff_multiplier == 2.0
    assert config.enable_metrics is True
    assert config.enable_health_check is True


def test_config_custom_values():
    """Should accept custom values."""
    config = OutboxConfig(
        batch_size=50,
        poll_interval_seconds=10,
        max_retry_count=5,
        retry_backoff_multiplier=3.0
    )
    
    assert config.batch_size == 50
    assert config.poll_interval_seconds == 10
    assert config.max_retry_count == 5
    assert config.retry_backoff_multiplier == 3.0


def test_config_batch_size_validation_min():
    """Should enforce minimum batch size."""
    with pytest.raises(ValidationError):
        OutboxConfig(batch_size=0)


def test_config_batch_size_validation_max():
    """Should enforce maximum batch size."""
    with pytest.raises(ValidationError):
        OutboxConfig(batch_size=1001)


def test_config_poll_interval_validation():
    """Should enforce poll interval range."""
    with pytest.raises(ValidationError):
        OutboxConfig(poll_interval_seconds=0)
    
    with pytest.raises(ValidationError):
        OutboxConfig(poll_interval_seconds=3601)


def test_config_retry_count_validation():
    """Should enforce retry count range."""
    with pytest.raises(ValidationError):
        OutboxConfig(max_retry_count=-1)
    
    with pytest.raises(ValidationError):
        OutboxConfig(max_retry_count=101)


def test_config_backoff_multiplier_validation():
    """Should enforce backoff multiplier range."""
    with pytest.raises(ValidationError):
        OutboxConfig(retry_backoff_multiplier=0.5)
    
    with pytest.raises(ValidationError):
        OutboxConfig(retry_backoff_multiplier=11.0)


def test_config_immutability():
    """Should be immutable after creation."""
    config = OutboxConfig()
    
    with pytest.raises(ValidationError):
        config.batch_size = 200


def test_config_edge_values():
    """Should accept valid edge values."""
    config = OutboxConfig(
        batch_size=1,  # Min
        poll_interval_seconds=3600,  # Max
        max_retry_count=0,  # Min
        retry_backoff_multiplier=1.0  # Min
    )
    
    assert config.batch_size == 1
    assert config.poll_interval_seconds == 3600
    assert config.max_retry_count == 0
    assert config.retry_backoff_multiplier == 1.0
