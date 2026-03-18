"""Native SQLAlchemy pagination strategy (fallback)."""

from typing import List, Optional, Type, Any
import math
from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from ..models import FilterSpec, SortSpec, PaginatedResult


class NativeStrategy:
    """Pagination strategy using native SQLAlchemy (zero dependencies)."""

    async def execute(
        self,
        db: AsyncSession,
        model_class: Type[DeclarativeBase],
        page: int,
        page_size: int,
        filters: Optional[List[FilterSpec]],
        sort: Optional[List[SortSpec]]
    ) -> PaginatedResult:
        """Execute paginated query using native SQLAlchemy."""
        query = select(model_class)

        # Apply filters
        if filters:
            for f in filters:
                query = self._apply_filter(query, model_class, f)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply sorting
        if sort:
            for s in sort:
                query = self._apply_sort(query, model_class, s)

        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)

        # Execute
        result = await db.execute(query)
        items = list(result.scalars().all())

        pages = math.ceil(total / page_size) if page_size > 0 else 0

        return PaginatedResult(
            items=items, total=total, page=page, page_size=page_size,
            pages=pages, has_next=page < pages, has_prev=page > 1
        )

    def _apply_filter(self, query: Any, model_class: Type, f: FilterSpec) -> Any:
        """Apply filter to query."""
        col = getattr(model_class, f.field)
        ops = {
            "eq": lambda: query.where(col == f.value),
            "ne": lambda: query.where(col != f.value),
            "gt": lambda: query.where(col > f.value),
            "gte": lambda: query.where(col >= f.value),
            "lt": lambda: query.where(col < f.value),
            "lte": lambda: query.where(col <= f.value),
            "in": lambda: query.where(col.in_(f.value)),
            "like": lambda: query.where(col.like(f"%{f.value}%")),
            "ilike": lambda: query.where(col.ilike(f"%{f.value}%")),
        }
        return ops.get(f.operator, lambda: query)()

    def _apply_sort(self, query: Any, model_class: Type, s: SortSpec) -> Any:
        """Apply sorting to query."""
        col = getattr(model_class, s.field)
        return query.order_by(desc(col) if s.direction == "desc" else asc(col))

