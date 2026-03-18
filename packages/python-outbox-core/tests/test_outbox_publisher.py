"""Property-based tests for OutboxPublisherBase.

Tests publish_batch, error handling, and metrics with mocks.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import AsyncMock
from python_outbox_core.publisher.base import OutboxPublisherBase
from python_outbox_core.publisher.error_handler import OutboxErrorHandler
from python_outbox_core.publisher.metrics import OutboxMetrics
from .conftest import SampleOutboxEvent


class ConcretePublisher(OutboxPublisherBase):
    """Concrete implementation for testing."""
    
    async def schedule_publishing(self) -> None:
        """Not used in tests."""
        pass


@given(batch_size=st.integers(min_value=1, max_value=50))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.asyncio
async def test_publish_batch_success(
    mock_repository, mock_publisher, sample_events, batch_size
):
    """Property: All events published successfully."""
    mock_repository.reset_mock()
    mock_publisher.reset_mock()
    
    events = sample_events[:batch_size]
    mock_repository.get_unpublished.return_value = events
    
    publisher = ConcretePublisher(mock_repository, mock_publisher)
    result = await publisher.publish_batch(limit=batch_size)
    
    assert result == batch_size
    assert mock_publisher.publish.call_count == batch_size
    assert mock_repository.mark_published.call_count == batch_size


@pytest.mark.asyncio
async def test_publish_batch_empty(mock_repository, mock_publisher):
    """Property: No events returns 0 without errors."""
    mock_repository.get_unpublished.return_value = []
    
    publisher = ConcretePublisher(mock_repository, mock_publisher)
    result = await publisher.publish_batch(limit=100)
    
    assert result == 0
    mock_publisher.publish.assert_not_called()
    mock_repository.mark_published.assert_not_called()


@given(
    batch_size=st.integers(min_value=5, max_value=20),
    fail_count=st.integers(min_value=1, max_value=10)
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.asyncio
async def test_publish_batch_partial_failures(
    mock_repository, mock_publisher, sample_events, batch_size, fail_count
):
    """Property: Partial failures logged, successful ones published."""
    mock_repository.reset_mock()
    mock_publisher.reset_mock()
    
    fail_count = min(fail_count, batch_size)
    events = sample_events[:batch_size]
    mock_repository.get_unpublished.return_value = events
    
    call_count = 0
    async def publish_side_effect(msg):
        nonlocal call_count
        call_count += 1
        if call_count <= fail_count:
            raise Exception("Publish failed")
    
    mock_publisher.publish.side_effect = publish_side_effect
    
    publisher = ConcretePublisher(mock_repository, mock_publisher)
    result = await publisher.publish_batch(limit=batch_size)
    
    assert result == batch_size - fail_count
    assert mock_publisher.publish.call_count == batch_size


@pytest.mark.asyncio
async def test_error_handler_logs_failures(
    mock_repository, mock_publisher, sample_events, mock_logger
):
    """Property: Error handler receives all failures."""
    events = sample_events[:3]
    mock_repository.get_unpublished.return_value = events
    mock_publisher.publish.side_effect = Exception("Test error")
    
    error_handler = OutboxErrorHandler(logger=mock_logger)
    publisher = ConcretePublisher(mock_repository, mock_publisher, error_handler)
    
    result = await publisher.publish_batch(limit=3)
    
    assert result == 0
    assert mock_logger.error.call_count == 3
