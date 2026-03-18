"""Message queue infrastructure exceptions."""

from .base import InfrastructureException


class MessageQueueError(InfrastructureException):
    """
    Message queue/broker infrastructure error.

    Use for:
    - Kafka broker unavailable
    - RabbitMQ connection failures
    - Message publish failures
    - Consumer group errors
    - Topic/queue not found

    Examples:
        raise MessageQueueError("Kafka broker unavailable", details="broker.example.com:9092")
        raise MessageQueueError("RabbitMQ connection failed", details="Connection refused")
        raise MessageQueueError("Message publish timeout", details="Topic: user-events")
    """

    def __init__(
        self,
        message: str,
        details: str = None,
        broker: str = None,
        topic: str = None
    ):
        """
        Initialize message queue error.

        Args:
            message: Human-readable error message
            details: Optional technical details
            broker: Optional broker type (e.g., "kafka", "rabbitmq")
            topic: Optional topic/queue name
        """
        self.broker = broker
        self.topic = topic
        super().__init__(message, details)

