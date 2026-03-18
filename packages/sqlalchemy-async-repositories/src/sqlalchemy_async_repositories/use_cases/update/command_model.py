"""Command model for update use case."""

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


class UpdateCommand(BaseModel):
    """Command: Update existing entity."""

    entity: DeclarativeBase

    class Config:
        arbitrary_types_allowed = True

