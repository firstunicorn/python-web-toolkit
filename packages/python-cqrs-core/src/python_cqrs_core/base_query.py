"""Base query with tracing and pagination fields."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from python_cqrs_core.query import IQuery


class BaseQuery(BaseModel, IQuery):
    """Base query with tracing fields.
    
    Provides common fields for observability.
    All queries should extend this class.
    
    Example:
        >>> class GetUserQuery(BaseQuery):
        ...     user_id: int
        >>> 
        >>> query = GetUserQuery(user_id=1, requested_by="admin")
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
        description="User or system that initiated the query"
    )
    requested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when query was created"
    )
    
    model_config = {"frozen": True}


class PaginatedQuery(BaseQuery):
    """Base query with pagination support.
    
    Extends BaseQuery with pagination fields.
    
    Example:
        >>> class ListUsersQuery(PaginatedQuery):
        ...     status: str = "active"
        >>> 
        >>> query = ListUsersQuery(page=2, page_size=20)
        >>> offset = query.offset  # 20
    """
    
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-indexed)"
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Items per page (1-100)"
    )
    
    @property
    def offset(self) -> int:
        """Calculate offset from page and page_size.
        
        Returns:
            Offset value for database queries
        
        Example:
            >>> query = PaginatedQuery(page=3, page_size=20)
            >>> query.offset
            40
        """
        return (self.page - 1) * self.page_size
