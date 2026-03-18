"""Unit tests for MessageQueueError.

Tests message queue infrastructure exceptions.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import MessageQueueError


class TestMessageQueueError:
    """Tests for MessageQueueError."""

    def test_message_queue_error_basic(self):
        """MessageQueueError should accept message."""
        exc = MessageQueueError("Kafka broker unavailable")
        assert "Kafka broker unavailable" in str(exc)

    def test_message_queue_error_with_broker(self):
        """MessageQueueError should accept broker parameter."""
        exc = MessageQueueError("Connection failed", broker="kafka")
        assert exc.broker == "kafka"

    def test_message_queue_error_with_topic(self):
        """MessageQueueError should accept topic parameter."""
        exc = MessageQueueError("Publish failed", topic="user-events")
        assert exc.topic == "user-events"
