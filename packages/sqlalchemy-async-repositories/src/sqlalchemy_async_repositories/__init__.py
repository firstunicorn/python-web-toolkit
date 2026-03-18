"""SQLAlchemy async repositories library.

Hybrid Approach:
- Basic CRUD: Native SQLAlchemy (fast, simple)
- Pagination/Filtering: FastCRUD if available, fallback to native
- Strategy Pattern: IPaginationStrategy protocol for extensibility
"""

from .interfaces import IRepository
from .base import BaseRepository
from .pagination import FilterSpec, SortSpec, PaginatedResult, has_fastcrud, IPaginationStrategy

__version__ = "0.1.0"

__all__ = [
    "IRepository",
    "BaseRepository",
    "FilterSpec",
    "SortSpec",
    "PaginatedResult",
    "has_fastcrud",
    "IPaginationStrategy",
]






