"""Command model for create use case."""

from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)


class CreateCommand(BaseModel):
    """Command: Create new entity."""

    entity: DeclarativeBase

    class Config:
        arbitrary_types_allowed = True

