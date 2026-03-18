"""Common API response DTOs."""

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field


T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response wrapper."""
    success: bool = True
    data: T
    message: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail model."""
    field: Optional[str] = Field(None, description="Field that caused error")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str = Field(..., description="Error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed errors")
    code: Optional[str] = Field(None, description="Error code")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    items: List[T]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total pages")


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True






