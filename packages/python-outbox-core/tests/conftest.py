"""Shared test fixtures for python-outbox-core.

Mock fixtures for testing publisher without real infrastructure.
RULE: Maximum 100 lines per file.
"""

import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from python_outbox_core.events import IOutboxEvent
from python_outbox_core.repository import IOutboxRepository
from python_outbox_core.publisher.interface import IEventPublisher


class SampleOutboxEvent(IOutboxEvent):
    """Concrete test event for testing."""
    
    def to_message(self):
        """Serialize to dict."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "occurred_at": self.occurred_at.isoformat(),
            "source": self.source
        }


@pytest.fixture
def mock_repository():
    """Mock outbox repository."""
    repo = AsyncMock(spec=IOutboxRepository)
    repo.get_unpublished.return_value = []
    repo.mark_published.return_value = None
    repo.mark_failed.return_value = None
    return repo


@pytest.fixture
def mock_publisher():
    """Mock event publisher."""
    publisher = AsyncMock(spec=IEventPublisher)
    publisher.publish.return_value = None
    return publisher


@pytest.fixture
def sample_events():
    """Create sample events for testing."""
    return [
        SampleOutboxEvent(
            event_id=uuid4(),
            event_type="test.event.created",
            aggregate_id=f"test_{i}",
            occurred_at=datetime.now(),
            source="test-service"
        )
        for i in range(50)
    ]


@pytest.fixture
def mock_logger():
    """Mock structlog logger."""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.error = MagicMock()
    logger.debug = MagicMock()
    return logger
