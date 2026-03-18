"""Pagination module - Strategy Pattern implementation."""

from .models import FilterSpec, SortSpec, PaginatedResult, has_fastcrud
from .strategies import IPaginationStrategy

__all__ = [
    "FilterSpec",
    "SortSpec",
    "PaginatedResult",
    "has_fastcrud",
    "IPaginationStrategy",
]

