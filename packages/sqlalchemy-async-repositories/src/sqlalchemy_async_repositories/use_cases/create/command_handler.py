"""Command handler for create use case."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class CreateHandler:
    """Handler for create command."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, entity: DeclarativeBase) -> DeclarativeBase:
        """
        Execute create command.

        Args:
            entity: Entity to create

        Returns:
            Created entity with ID populated
        """
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

