"""Query handler for get_by_id use case."""

from typing import Optional, Any, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class GetByIdHandler:
    """Handler for get_by_id query."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        self.db = db
        self.model_class = model_class

    async def execute(self, entity_id: Any) -> Optional[DeclarativeBase]:
        """
        Execute get_by_id query.

        Args:
            entity_id: ID of entity to retrieve

        Returns:
            Entity if found, None otherwise
        """
        result = await self.db.execute(
            select(self.model_class).where(self.model_class.id == entity_id)
        )
        return result.scalar_one_or_none()

