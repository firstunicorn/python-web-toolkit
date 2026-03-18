"""Pagination router - Strategy Pattern selector."""

from typing import Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .models import FilterSpec, SortSpec, PaginatedResult, has_fastcrud
from .strategies.fastcrud_strategy import FastCRUDStrategy
from .strategies.native_strategy import NativeStrategy


class PaginationRouter:
    """
    Routes pagination requests to appropriate strategy.

    Strategy Pattern:
    - FastCRUD if available (preferred)
    - Native SQLAlchemy (fallback)
    """

    def __init__(self):
        self._strategy = FastCRUDStrategy() if has_fastcrud() else NativeStrategy()

    async def find_paginated(
        self,
        db: AsyncSession,
        model_class: Type[DeclarativeBase],
        page: int,
        page_size: int,
        filters: Optional[List[FilterSpec]],
        sort: Optional[List[SortSpec]]
    ) -> PaginatedResult:
        """Execute paginated query using selected strategy."""
        return await self._strategy.execute(
            db, model_class, page, page_size, filters, sort
        )

