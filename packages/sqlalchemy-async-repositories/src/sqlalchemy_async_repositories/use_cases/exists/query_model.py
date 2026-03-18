"""Query model for exists use case."""

from typing import Any
from pydantic import BaseModel


class ExistsQuery(BaseModel):
    """Query: Check if entity exists by ID."""

    entity_id: Any

    class Config:
        arbitrary_types_allowed = True

