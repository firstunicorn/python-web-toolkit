"""
Metrics and observability for outbox publishing.

Best Practices Applied:
1. Structured logging (machine-readable)
2. Consistent event naming (outbox.*)
3. Rich context (event_id, type, timing)
4. OpenTelemetry-ready structure

References:
- Structured logging: https://www.structlog.org/
"""

import structlog
from typing import Any


class OutboxMetrics:
    """
    Structured logging for outbox operations.

    Projects can extend this to add Prometheus/StatsD metrics.
    """

    def __init__(self, logger: Any = None):
        """
        Initialize metrics logger.

        Args:
            logger: structlog logger instance (creates default if None)
        """
        self.logger = logger or structlog.get_logger(__name__)

    def log_no_events(self) -> None:
        """Log when no events are pending."""
        self.logger.debug("outbox.no_events_to_publish")

    def log_success(self, event: Any) -> None:
        """
        Log successful event publication.

        Args:
            event: The published IOutboxEvent instance
        """
        self.logger.info(
            "outbox.event_published",
            event_id=str(event.event_id),
            event_type=event.event_type,
            aggregate_id=event.aggregate_id,
        )

    def log_batch_complete(self, published: int, total: int) -> None:
        """
        Log batch processing completion.

        Args:
            published: Number of successfully published events
            total: Total events in batch
        """
        self.logger.info(
            "outbox.batch_complete",
            published=published,
            total=total,
            success_rate=published / total if total > 0 else 0,
        )

    def log_batch_started(self, batch_size: int) -> None:
        """Log batch processing start."""
        self.logger.debug("outbox.batch_started", batch_size=batch_size)

