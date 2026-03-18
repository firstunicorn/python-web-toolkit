"""Command model for delete use case."""

from typing import Any
from pydantic import BaseModel


class DeleteCommand(BaseModel):
    """Command: Delete entity by ID."""

    entity_id: Any

    class Config:
        arbitrary_types_allowed = True

