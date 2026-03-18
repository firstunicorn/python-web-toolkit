"""
Base interface for outbox events.

Best Practices Applied:
1. ABC for contract enforcement
2. Pydantic for validation & serialization
3. Standard event metadata (CloudEvents-inspired)
4. Type safety with generics
5. Immutability encouraged (frozen=True optional)

References:
- CloudEvents spec: https://cloudevents.io/
- Domain Event pattern: https://martinfowler.com/eaaDev/DomainEvent.html
"""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from typing import Any
from pydantic import BaseModel, Field


class IOutboxEvent(BaseModel, ABC):
    """
    Abstract base for all outbox events.

    Enforces event metadata standards and serialization contract.
    Projects extend this for domain-specific events.

    Metadata fields follow CloudEvents specification for interoperability.
    """

    event_id: UUID
    """Unique identifier for this event (idempotency key)."""

    event_type: str
    """Event type in reverse-DNS format (e.g. 'com.gridflow.invite.created')."""

    aggregate_id: str
    """ID of the aggregate root that produced this event."""

    occurred_at: datetime
    """When the event occurred (domain time, not system time)."""

    source: str
    """Service/application that produced this event (e.g. 'user-service')."""

    data_version: str = "1.0"
    """Event schema version for evolution/compatibility (semver recommended)."""

    correlation_id: UUID | None = None
    """Links related events across service boundaries."""

    causation_id: UUID | None = None
    """ID of the event/command that caused this event."""

    @abstractmethod
    def to_message(self) -> dict[str, Any]:
        """
        Serialize event to Kafka message format.

        Must return a JSON-serializable dict for publishing.
        Override to customize serialization (e.g., omit fields, transform data).
        """
        ...

    def get_partition_key(self) -> str:
        """Return partition key for Kafka routing.

        Default: aggregate_id (natural partition key).
        Override for custom routing (e.g., user_id, tenant_id).

        Best practice: Use 3-10 topics with partition keys,
        NOT hundreds of topics per entity.

        Returns:
            Partition key string for Kafka producer
        """
        return self.aggregate_id

    class Config:
        """Pydantic config for event models."""

        # Ensure datetime is serialized to ISO format
        json_encoders = {datetime: lambda v: v.isoformat()}

        # Allow frozen for immutability (optional, project-specific)
        # frozen = True

