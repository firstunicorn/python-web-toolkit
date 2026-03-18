"""Command handler for update use case."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class UpdateHandler:
    """Handler for update command."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, entity: DeclarativeBase) -> DeclarativeBase:
        """
        Execute update command.

        Args:
            entity: Entity to update (must have existing ID)

        Returns:
            Updated entity
        """
        merged = await self.db.merge(entity)
        await self.db.flush()
        await self.db.refresh(merged)
        return merged

