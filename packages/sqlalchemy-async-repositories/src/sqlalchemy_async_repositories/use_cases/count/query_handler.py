"""Query handler for count use case."""

from typing import Type
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class CountHandler:
    """Handler for count query."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        self.db = db
        self.model_class = model_class

    async def execute(self) -> int:
        """
        Execute count query.

        Returns:
            Total number of entities
        """
        result = await self.db.execute(
            select(func.count()).select_from(self.model_class)
        )
        return result.scalar() or 0

