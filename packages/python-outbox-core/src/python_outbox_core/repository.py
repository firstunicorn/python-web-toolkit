"""
Repository interface for outbox persistence.

Best Practices Applied:
1. Repository pattern for data access abstraction
2. Async/await for non-blocking I/O
3. Batch operations for performance
4. Pagination support
5. Compatible with SQLAlchemy's Unit of Work (AsyncSession)

References:
- Repository pattern: https://martinfowler.com/eaaCatalog/repository.html
- Unit of Work: https://martinfowler.com/eaaCatalog/unitOfWork.html
"""

from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from .events import IOutboxEvent


class IOutboxRepository(ABC):
    """
    Abstract repository for outbox event persistence.

    Implementations use SQLAlchemy AsyncSession for actual DB operations.
    This interface is intentionally minimal - projects extend as needed.
    """

    @abstractmethod
    async def add_event(self, event: IOutboxEvent) -> None:
        """
        Add event to outbox table.

        IMPORTANT: Does NOT commit transaction.
        Caller must commit via AsyncSession for atomicity.

        Args:
            event: Domain event to store in outbox

        Raises:
            DatabaseError: On persistence failures
        """
        ...

    @abstractmethod
    async def get_unpublished(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[IOutboxEvent]:
        """
        Fetch unpublished events for worker processing.

        Args:
            limit: Max events to return (batch size)
            offset: Pagination offset

        Returns:
            List of unpublished events, ordered by occurred_at ASC
        """
        ...

    @abstractmethod
    async def mark_published(self, event_id: UUID) -> None:
        """
        Mark event as successfully published to Kafka.

        Args:
            event_id: ID of the published event

        Raises:
            DatabaseError: On update failures
        """
        ...

    @abstractmethod
    async def count_unpublished(self) -> int:
        """
        Count pending events for monitoring.

        Used for:
        - Health checks
        - Alerting on lag
        - Capacity planning

        Returns:
            Number of unpublished events
        """
        ...

    @abstractmethod
    async def mark_failed(self, event_id: UUID, error_message: str) -> None:
        """
        Mark event as permanently failed (Dead Letter Queue).

        Used when:
        - Event cannot be published after max retries
        - Event payload is invalid
        - Broker rejects the event

        Args:
            event_id: ID of the failed event
            error_message: Why it failed (for debugging)

        Raises:
            DatabaseError: On update failures
        """
        ...

