"""Pagination, filtering, and sorting utilities.

Hybrid approach:
- Uses FastCRUD if available (battle-tested, feature-rich)
- Falls back to native SQLAlchemy (simple, no dependencies)
"""

from typing import Generic, TypeVar, List, Any, Optional, Literal
from pydantic import BaseModel, Field
import math

T = TypeVar('T')


class FilterSpec(BaseModel):
    """Filter specification for queries."""
    field: str
    operator: Literal["eq", "ne", "gt", "gte", "lt", "lte", "in", "like", "ilike"]
    value: Any


class SortSpec(BaseModel):
    """Sort specification for queries."""
    field: str
    direction: Literal["asc", "desc"] = "asc"


class PaginatedResult(BaseModel, Generic[T]):
    """Paginated result with metadata."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool

    class Config:
        arbitrary_types_allowed = True


# Try to import FastCRUD (optional dependency)
try:
    from fastcrud import FastCRUD
    HAS_FASTCRUD = True
except ImportError:
    HAS_FASTCRUD = False
    FastCRUD = None  # type: ignore


def has_fastcrud() -> bool:
    """Check if FastCRUD is available."""
    return HAS_FASTCRUD

