"""Pagination data models."""

from typing import TypeVar, Generic, List, Any
from pydantic import BaseModel

# Try importing FastCRUD, set flag if not available
try:
    from fastcrud import FastCRUD
    _has_fastcrud = True
except ImportError:
    FastCRUD = Any  # Type hint for when FastCRUD is not installed
    _has_fastcrud = False


def has_fastcrud() -> bool:
    """Check if FastCRUD is installed."""
    return _has_fastcrud


T = TypeVar('T')


class FilterSpec(BaseModel):
    """Specification for filtering queries."""
    field: str
    operator: str  # "eq", "ne", "gt", "gte", "lt", "lte", "like", "ilike", "in"
    value: Any


class SortSpec(BaseModel):
    """Specification for sorting queries."""
    field: str
    direction: str = "asc"  # "asc" or "desc"


class PaginatedResult(BaseModel, Generic[T]):
    """Generic paginated result structure."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool
    
    model_config = {"arbitrary_types_allowed": True}

