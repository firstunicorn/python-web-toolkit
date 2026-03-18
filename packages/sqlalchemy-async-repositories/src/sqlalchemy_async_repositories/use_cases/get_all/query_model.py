"""Query model for get_all use case."""

from typing import Optional
from pydantic import BaseModel, Field


class GetAllQuery(BaseModel):
    """Query: Get all entities with optional pagination."""

    limit: Optional[int] = Field(None, ge=1, description="Maximum results")
    offset: int = Field(0, ge=0, description="Number of results to skip")

