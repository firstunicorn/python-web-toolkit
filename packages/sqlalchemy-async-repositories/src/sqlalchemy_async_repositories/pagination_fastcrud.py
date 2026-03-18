"""FastCRUD implementation for pagination (used when available)."""

"""
DEPRECATED: Moved to pagination/strategies/fastcrud_strategy.py

Kept for backwards compatibility.
"""

from typing import List, Optional, Any
import math

from .pagination.models import FilterSpec, SortSpec, PaginatedResult


async def find_paginated_fastcrud(
    fastcrud_instance: Any,
    db_session: Any,
    page: int,
    page_size: int,
    filters: Optional[List[FilterSpec]],
    sort: Optional[List[SortSpec]]
) -> PaginatedResult:
    """
    Paginated query using FastCRUD.

    This is used when FastCRUD is installed (optional dependency).
    Provides battle-tested pagination with advanced features.
    """
    # Convert our FilterSpec to FastCRUD format
    fastcrud_filters = {}
    if filters:
        for filter_spec in filters:
            # FastCRUD uses dict format: {field: {operator: value}}
            if filter_spec.field not in fastcrud_filters:
                fastcrud_filters[filter_spec.field] = {}

            # Map our operators to FastCRUD operators
            operator_map = {
                "eq": "__eq",
                "ne": "__ne",
                "gt": "__gt",
                "gte": "__gte",
                "lt": "__lt",
                "lte": "__lte",
                "in": "__in",
                "like": "__like",
                "ilike": "__ilike",
            }

            fastcrud_op = operator_map.get(filter_spec.operator, "__eq")
            fastcrud_filters[filter_spec.field][fastcrud_op] = filter_spec.value

    # Convert our SortSpec to FastCRUD format
    sort_columns = [s.field for s in (sort or [])]
    sort_orders = [s.direction for s in (sort or [])]

    # Call FastCRUD
    result = await fastcrud_instance.get_multi(
        db=db_session,
        offset=(page - 1) * page_size,
        limit=page_size,
        sort_columns=sort_columns if sort_columns else None,
        sort_orders=sort_orders if sort_orders else None,
        **fastcrud_filters
    )

    # Convert to our standard format
    total = result.get("total_count", 0)
    pages = math.ceil(total / page_size) if page_size > 0 else 0

    return PaginatedResult(
        items=result.get("data", []),
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

