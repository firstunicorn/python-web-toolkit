"""Query model for find_paginated use case."""

from typing import Optional, List
from pydantic import BaseModel, Field

from ...pagination.models import FilterSpec, SortSpec


class FindPaginatedQuery(BaseModel):
    """Query: Find entities with pagination, filtering, and sorting."""

    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(10, ge=1, le=1000, description="Items per page")
    filters: Optional[List[FilterSpec]] = Field(None, description="Filter criteria")
    sort: Optional[List[SortSpec]] = Field(None, description="Sort criteria")

