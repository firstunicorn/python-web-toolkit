"""FastCRUD pagination strategy."""

from typing import List, Optional, Type, Any
import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

try:
    from fastcrud import FastCRUD
    _has_fastcrud = True
except ImportError:
    _has_fastcrud = False

from ..models import FilterSpec, SortSpec, PaginatedResult


class FastCRUDStrategy:
    """Pagination strategy using FastCRUD library."""

    def __init__(self):
        if not _has_fastcrud:
            raise ImportError("FastCRUD not installed")

    async def execute(
        self,
        db: AsyncSession,
        model_class: Type[DeclarativeBase],
        page: int,
        page_size: int,
        filters: Optional[List[FilterSpec]],
        sort: Optional[List[SortSpec]]
    ) -> PaginatedResult:
        """Execute paginated query using FastCRUD."""
        fastcrud = FastCRUD(model_class)

        # Convert FilterSpec to FastCRUD format
        fastcrud_filters = self._convert_filters(filters)

        # Convert SortSpec to FastCRUD format
        sort_columns = [s.field for s in (sort or [])]
        sort_orders = [s.direction for s in (sort or [])]

        # Execute FastCRUD query
        result = await fastcrud.get_multi(
            db=db,
            offset=(page - 1) * page_size,
            limit=page_size,
            sort_columns=sort_columns if sort_columns else None,
            sort_orders=sort_orders if sort_orders else None,
            **fastcrud_filters
        )

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

    def _convert_filters(self, filters: Optional[List[FilterSpec]]) -> dict:
        """Convert FilterSpec list to FastCRUD format."""
        if not filters:
            return {}

        fastcrud_filters = {}
        operator_map = {
            "eq": "__eq", "ne": "__ne",
            "gt": "__gt", "gte": "__gte",
            "lt": "__lt", "lte": "__lte",
            "in": "__in", "like": "__like", "ilike": "__ilike",
        }

        for f in filters:
            if f.field not in fastcrud_filters:
                fastcrud_filters[f.field] = {}
            op = operator_map.get(f.operator, "__eq")
            fastcrud_filters[f.field][op] = f.value

        return fastcrud_filters

