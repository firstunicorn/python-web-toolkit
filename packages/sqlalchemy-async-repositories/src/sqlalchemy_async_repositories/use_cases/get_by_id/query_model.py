"""Query model for get_by_id use case."""

from typing import Any
from pydantic import BaseModel


class GetByIdQuery(BaseModel):
    """Query: Get entity by ID."""

    entity_id: Any

    class Config:
        arbitrary_types_allowed = True

