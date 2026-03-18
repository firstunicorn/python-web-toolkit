"""Protocol for pagination strategies (Strategy Pattern).

This defines the interface that all pagination strategies must implement.
Using Protocol (PEP 544) for structural subtyping - no inheritance needed.
"""

from typing import Protocol, Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from ..models import FilterSpec, SortSpec, PaginatedResult


class IPaginationStrategy(Protocol):
    """
    Protocol for pagination strategies.

    Implementations:
    - FastCRUDStrategy: Uses FastCRUD library (battle-tested, feature-rich)
    - NativeStrategy: Uses native SQLAlchemy (zero dependencies, fallback)

    Why Protocol?
    - Type-safe without inheritance
    - Easy to test (mock the protocol)
    - Clear interface contract
    - IDE autocomplete support
    """

    async def execute(
        self,
        db: AsyncSession,
        model_class: Type[DeclarativeBase],
        page: int,
        page_size: int,
        filters: Optional[List[FilterSpec]],
        sort: Optional[List[SortSpec]]
    ) -> PaginatedResult:
        """
        Execute paginated query.

        Args:
            db: Async database session
            model_class: SQLAlchemy model class
            page: Page number (1-indexed)
            page_size: Items per page
            filters: List of filter specifications
            sort: List of sort specifications

        Returns:
            PaginatedResult with items and metadata
        """
        ...


