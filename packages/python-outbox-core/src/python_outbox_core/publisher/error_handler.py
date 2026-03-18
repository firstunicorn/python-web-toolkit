"""
Error handling for outbox event publishing.

Best Practices Applied:
1. Separation of concerns (error handling isolated)
2. Rich error context for debugging
3. Retry decision logic (extensible)
4. Dead Letter Queue (DLQ) support

References:
- Error handling patterns: https://aws.amazon.com/message-queue/features/dead-letter-queues/
"""

import structlog
from typing import Any


class OutboxErrorHandler:
    """
    Handles per-event publishing errors.

    Projects can extend this for custom retry/DLQ logic.
    """

    def __init__(self, logger: Any = None, max_retries: int = 3):
        """
        Initialize error handler.

        Args:
            logger: structlog logger instance
            max_retries: Max retries before marking failed
        """
        self.logger = logger or structlog.get_logger(__name__)
        self.max_retries = max_retries

    def handle(self, event: Any, exception: Exception) -> None:
        """
        Log error with full context.

        Args:
            event: The failed IOutboxEvent instance
            exception: The exception that was raised
        """
        self.logger.error(
            "outbox.publish_failed",
            event_id=str(event.event_id),
            event_type=event.event_type,
            aggregate_id=event.aggregate_id,
            error=str(exception),
            error_type=type(exception).__name__,
            exc_info=True,
        )

    def should_retry(self, event: Any, exception: Exception, attempt: int) -> bool:
        """
        Decide if event should be retried.

        Override for custom retry logic (e.g., skip retries for validation errors).

        Args:
            event: The failed IOutboxEvent instance
            exception: The exception that was raised
            attempt: Current attempt number (0-indexed)

        Returns:
            True if should retry, False to mark failed (DLQ)
        """
        return attempt < self.max_retries

    def is_transient_error(self, exception: Exception) -> bool:
        """
        Check if error is transient (network, timeout, etc.).

        Override to customize transient error detection.
        """
        # Default: retry all errors (projects can override)
        return True

