"""Base class for internal domain events."""

from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseDomainEvent(BaseModel):
    """
    Base class for internal domain events (in-process).
    
    Use for same-service side effects:
    - Send emails
    - Update caches
    - Log activities
    - Trigger workflows
    
    For cross-service events, use IOutboxEvent from python-outbox-core.
    """
    
    model_config = ConfigDict(
        frozen=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    )
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    correlation_id: Optional[UUID] = None
    causation_id: Optional[UUID] = None
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
