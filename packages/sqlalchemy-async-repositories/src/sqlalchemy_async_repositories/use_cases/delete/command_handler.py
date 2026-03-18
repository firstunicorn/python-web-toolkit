"""Command handler for delete use case."""

from typing import Any, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class DeleteHandler:
    """Handler for delete command."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        self.db = db
        self.model_class = model_class

    async def execute(self, entity_id: Any) -> bool:
        """
        Execute delete command.

        Args:
            entity_id: ID of entity to delete

        Returns:
            True if deleted, False if not found
        """
        result = await self.db.execute(
            select(self.model_class).where(self.model_class.id == entity_id)
        )
        entity = result.scalar_one_or_none()

        if not entity:
            return False

        await self.db.delete(entity)
        await self.db.flush()
        return True

