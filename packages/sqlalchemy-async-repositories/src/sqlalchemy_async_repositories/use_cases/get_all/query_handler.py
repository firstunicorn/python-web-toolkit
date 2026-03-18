"""Query handler for get_all use case."""

from typing import List, Optional, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class GetAllHandler:
    """Handler for get_all query."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeBase]):
        self.db = db
        self.model_class = model_class

    async def execute(
        self,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[DeclarativeBase]:
        """
        Execute get_all query.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of entities
        """
        query = select(self.model_class).offset(offset)

        if limit:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

