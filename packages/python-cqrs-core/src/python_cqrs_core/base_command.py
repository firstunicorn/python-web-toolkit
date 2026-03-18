"""Base command with tracing and audit fields."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from python_cqrs_core.command import ICommand


class BaseCommand(BaseModel, ICommand):
    """Base command with tracing and audit fields.
    
    Provides common fields for observability and audit trail.
    All commands should extend this class.
    
    Example:
        >>> class CreateUserCommand(BaseCommand):
        ...     name: str
        ...     email: str
        >>> 
        >>> cmd = CreateUserCommand(
        ...     name="John",
        ...     email="john@example.com",
        ...     requested_by="admin"
        ... )
    """
    
    request_id: UUID = Field(
        default_factory=uuid4,
        description="Unique request identifier"
    )
    correlation_id: Optional[UUID] = Field(
        default=None,
        description="Correlation ID for distributed tracing"
    )
    requested_by: Optional[str] = Field(
        default=None,
        description="User or system that initiated the command"
    )
    requested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when command was created"
    )
    
    model_config = {"frozen": True}
