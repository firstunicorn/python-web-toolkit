"""Query handler for exists use case."""

from typing import Any, Type
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class ExistsHandler:
    """Handler for exists query."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        self.db = db
        self.model_class = model_class

    async def execute(self, entity_id: Any) -> bool:
        """
        Execute exists query.

        Args:
            entity_id: ID to check

        Returns:
            True if entity exists, False otherwise
        """
        result = await self.db.execute(
            select(func.count(self.model_class.id)).where(
                self.model_class.id == entity_id
            )
        )
        return (result.scalar() or 0) > 0

