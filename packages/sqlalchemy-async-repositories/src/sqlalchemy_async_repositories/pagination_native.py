"""
DEPRECATED: Moved to pagination/strategies/native_strategy.py

Kept for backwards compatibility.
"""

from typing import List, Optional, Type, Any
from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
import math

from .pagination.models import FilterSpec, SortSpec, PaginatedResult


async def find_paginated_native(
    db_session: AsyncSession,
    model_class: Type[DeclarativeBase],
    page: int,
    page_size: int,
    filters: Optional[List[FilterSpec]],
    sort: Optional[List[SortSpec]]
) -> PaginatedResult:
    """
    Paginated query using native SQLAlchemy.

    This is the fallback when FastCRUD is not installed.
    Simple, fast, zero external dependencies.
    """
    query = select(model_class)

    # Apply filters
    if filters:
        for filter_spec in filters:
            query = _apply_filter(query, model_class, filter_spec)

    # Get total count (before pagination)
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db_session.execute(count_query)
    total = count_result.scalar() or 0

    # Apply sorting
    if sort:
        for sort_spec in sort:
            query = _apply_sort(query, model_class, sort_spec)

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute query
    result = await db_session.execute(query)
    items = list(result.scalars().all())

    # Calculate pagination metadata
    pages = math.ceil(total / page_size) if page_size > 0 else 0

    return PaginatedResult(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )


def _apply_filter(query: Any, model_class: Type, filter_spec: FilterSpec) -> Any:
    """Apply filter to query."""
    column = getattr(model_class, filter_spec.field)

    if filter_spec.operator == "eq":
        return query.where(column == filter_spec.value)
    elif filter_spec.operator == "ne":
        return query.where(column != filter_spec.value)
    elif filter_spec.operator == "gt":
        return query.where(column > filter_spec.value)
    elif filter_spec.operator == "gte":
        return query.where(column >= filter_spec.value)
    elif filter_spec.operator == "lt":
        return query.where(column < filter_spec.value)
    elif filter_spec.operator == "lte":
        return query.where(column <= filter_spec.value)
    elif filter_spec.operator == "in":
        return query.where(column.in_(filter_spec.value))
    elif filter_spec.operator == "like":
        return query.where(column.like(f"%{filter_spec.value}%"))
    elif filter_spec.operator == "ilike":
        return query.where(column.ilike(f"%{filter_spec.value}%"))

    return query


def _apply_sort(query: Any, model_class: Type, sort_spec: SortSpec) -> Any:
    """Apply sorting to query."""
    column = getattr(model_class, sort_spec.field)

    if sort_spec.direction == "desc":
        return query.order_by(desc(column))
    else:
        return query.order_by(asc(column))

