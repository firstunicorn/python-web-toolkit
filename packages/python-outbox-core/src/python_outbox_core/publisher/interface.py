"""
Event publisher interface.

Best Practices Applied:
1. Interface Segregation Principle (single responsibility)
2. Broker-agnostic (Kafka, RabbitMQ, etc.)
3. Async/await for non-blocking I/O
4. Simple contract for easy testing

References:
- ISP: https://en.wikipedia.org/wiki/Interface_segregation_principle
"""

from abc import ABC, abstractmethod
from typing import Any


class IEventPublisher(ABC):
    """
    Interface for event publishing (Kafka, RabbitMQ, etc.).

    Projects implement this for their specific message broker.
    Keeps outbox library broker-agnostic.

    Example implementations:
    - KafkaPublisher (via FastStream)
    - RabbitMQPublisher (via aio-pika)
    - SQSPublisher (via aiobotocore)
    """

    @abstractmethod
    async def publish(self, message: dict[str, Any]) -> None:
        """
        Publish event to message broker.

        Implementation must handle:
        - Connection management
        - Serialization (if needed beyond JSON)
        - Retry logic (or delegate to Tenacity)
        - Topic/exchange routing

        Args:
            message: JSON-serializable event payload

        Raises:
            PublishError: On transient/permanent publish failures
        """
        ...

