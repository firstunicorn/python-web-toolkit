"""
Base publisher/worker for outbox event publishing.

Best Practices Applied:
1. Template Method pattern - reusable core, custom schedule
2. Batch processing for efficiency
3. Dependency injection for error handling & metrics; error handling with structured logging
4. Single Responsibility - only batch orchestration; only publishes, doesn't schedule
5. Open/Closed principle - extend, don't modify

References:
- Template Method: https://refactoring.guru/design-patterns/template-method
- Competing Consumers: https://www.enterpriseintegrationpatterns.com/patterns/messaging/CompetingConsumers.html
"""

from abc import ABC, abstractmethod

from ..repository import IOutboxRepository
from .interface import IEventPublisher
from .error_handler import OutboxErrorHandler
from .metrics import OutboxMetrics


class OutboxPublisherBase(ABC):
    """
    Reusable outbox worker logic.

    Handles:
    - Batch fetching from outbox
    - Publishing to broker (via IEventPublisher)
    - Marking events as published (via IOutboxRepository)
    - Error handling (via OutboxErrorHandler)
    - Metrics/logging (via OutboxMetrics)

    Projects extend this and implement schedule_publishing().
    """

    def __init__(
        self,
        repository: IOutboxRepository,
        publisher: IEventPublisher,
        error_handler: OutboxErrorHandler | None = None,
        metrics: OutboxMetrics | None = None,
    ):
        """
        Initialize outbox publisher.

        Args:
            repository: Outbox repository for DB operations
            publisher: Event publisher (Kafka/FastStream)
            error_handler: Error handling strategy (creates default if None)
            metrics: Metrics logger (creates default if None)
        """
        self.repository = repository
        self.publisher = publisher
        self.error_handler = error_handler or OutboxErrorHandler()
        self.metrics = metrics or OutboxMetrics()

    async def publish_batch(self, limit: int = 100) -> int:
        """
        Fetch and publish a batch of unpublished events.

        Args:
            limit: Max events to process in this batch

        Returns:
            Number of successfully published events
        """
        events = await self.repository.get_unpublished(limit=limit)

        if not events:
            self.metrics.log_no_events()
            return 0

        self.metrics.log_batch_started(len(events))
        published_count = 0

        for event in events:
            if await self._try_publish(event):
                published_count += 1

        self.metrics.log_batch_complete(published_count, len(events))
        return published_count

    async def _try_publish(self, event) -> bool:
        """
        Publish one event with error handling.

        Returns:
            True if published successfully, False otherwise
        """
        try:
            message = event.to_message()
            await self.publisher.publish(message)
            await self.repository.mark_published(event.event_id)
            self.metrics.log_success(event)
            return True
        except Exception as exc:
            self.error_handler.handle(event, exc)
            return False

    @abstractmethod
    async def schedule_publishing(self) -> None:
        """
        Implement your scheduling strategy.

        Options:
        - Infinite loop: while True + asyncio.sleep()
        - Celery beat: Distributed scheduling
        - K8s CronJob: Container-based scheduling
        """
        ...
