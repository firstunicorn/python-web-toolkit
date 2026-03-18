"""
Query handler for find_paginated use case.

Architecture Patterns:
- CQRS Pattern: Query-side handler for paginated reads
- Strategy Pattern: Delegates to IPaginationStrategy (FastCRUD or Native)
- Factory Pattern: Uses PaginationStrategyFactory for strategy creation
- Protocol Pattern: IPaginationStrategy defines type-safe interface (PEP 544)

Pattern Interactions:
1. Factory creates appropriate strategy at init
2. Strategy delegates execution to implementation (FastCRUD or Native)
3. Protocol ensures type safety without inheritance
4. Handler coordinates patterns without implementing business logic
"""

from typing import Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from ...pagination.models import FilterSpec, SortSpec, PaginatedResult
from ...pagination.strategies import IPaginationStrategy
from .strategy_factory import PaginationStrategyFactory


class FindPaginatedHandler:
    """
    Handler for find_paginated query using Strategy + Factory patterns.

    Responsibilities:
    - Coordinate pagination request
    - Delegate to appropriate strategy (via Factory)
    - Return standardized PaginatedResult

    Does NOT:
    - Implement pagination logic (delegated to strategies)
    - Decide which strategy to use (delegated to factory)
    """

    strategy: IPaginationStrategy  # ✅ Type-hinted via Protocol

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        """
        Initialize handler with database session and model.

        Args:
            db: Async database session
            model_class: SQLAlchemy model class to query
        """
        self.db = db
        self.model_class = model_class
        # ✅ Factory Pattern: Delegates strategy creation
        self.strategy: IPaginationStrategy = PaginationStrategyFactory.create()

    def get_backend_info(self) -> dict:
        """
        Get current pagination backend info (debugging/monitoring).

        Returns:
            dict: Backend metadata (name, class, availability)

        Example:
            >>> handler = FindPaginatedHandler(session, UserORM)
            >>> info = handler.get_backend_info()
            >>> print(info["backend"])  # "FastCRUD" or "Native"
        """
        return {
            "backend": PaginationStrategyFactory.get_backend_name(self.strategy),
            "strategy_class": self.strategy.__class__.__name__,
            "has_fastcrud_available": PaginationStrategyFactory.is_fastcrud_available()
        }

    async def execute(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[List[FilterSpec]] = None,
        sort: Optional[List[SortSpec]] = None
    ) -> PaginatedResult:
        """
        Execute find_paginated query using selected strategy.

        Args:
            page: Page number (1-indexed)
            page_size: Items per page
            filters: Filter specifications
            sort: Sort specifications

        Returns:
            PaginatedResult: Paginated result with items and metadata
        """
        # ✅ Direct strategy call (no router wrapper)
        return await self.strategy.execute(
            self.db,
            self.model_class,
            page,
            page_size,
            filters,
            sort
        )

