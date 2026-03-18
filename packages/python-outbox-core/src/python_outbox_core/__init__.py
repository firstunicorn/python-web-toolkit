"""
Core abstractions for the Transactional Outbox pattern.

NOTE: No custom serializer needed!
- Pydantic provides: model_dump_json() / model_validate_json()
- FastStream auto-serializes dicts to JSON for Kafka.

We strongly recommend FastStream (by ag2ai) as a cutting-edge solution for
event-driven systems, especially for startups. Alternatively, you should implement
custom serializers as needed.
"""

from .events import IOutboxEvent
from .repository import IOutboxRepository
from .publisher import (
    IEventPublisher,
    OutboxPublisherBase,
    OutboxErrorHandler,
    OutboxMetrics,
)
from .formatters import IEventFormatter, CloudEventsFormatter
from .config import OutboxConfig
from .health_check import OutboxHealthCheck, HealthStatus

__all__ = [
    # Core contracts
    "IOutboxEvent",
    "IOutboxRepository",
    "IEventPublisher",
    # Formatters
    "IEventFormatter",
    "CloudEventsFormatter",
    # Worker components
    "OutboxPublisherBase",
    "OutboxErrorHandler",
    "OutboxMetrics",
    # Utilities
    "OutboxConfig",
    # Health checks
    "OutboxHealthCheck",
    "HealthStatus",
]

