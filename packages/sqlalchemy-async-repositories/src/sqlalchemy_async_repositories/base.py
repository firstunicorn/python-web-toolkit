"""Base repository - orchestrates use case handlers.

Architecture:
- use_cases/ - Query/Command handlers organized by use case
- pagination/ - Strategy Pattern for pagination backends
"""

from typing import TypeVar, Generic, Optional, List, Any, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .interfaces import IRepository
from .pagination.models import FilterSpec, SortSpec, PaginatedResult

# Import use case handlers
from .use_cases.get_by_id.query_handler import GetByIdHandler
from .use_cases.get_all.query_handler import GetAllHandler
from .use_cases.exists.query_handler import ExistsHandler
from .use_cases.count.query_handler import CountHandler
from .use_cases.create.command_handler import CreateHandler
from .use_cases.update.command_handler import UpdateHandler
from .use_cases.delete.command_handler import DeleteHandler
from .use_cases.find_paginated.query_handler import FindPaginatedHandler

T = TypeVar('T', bound=DeclarativeBase)


class BaseRepository(IRepository[T], Generic[T]):
    """
    Base repository orchestrating use case handlers.

    Structure mirrors GridFlow conventions:
    - use_cases/{use_case_name}/query_handler.py
    - use_cases/{use_case_name}/command_handler.py
    - use_cases/{use_case_name}/query_model.py
    - use_cases/{use_case_name}/command_model.py
    """

    def __init__(self, db_session: AsyncSession, model_class: Type[T]):
        self.db = db_session
        self.model_class = model_class

        # Initialize handlers (lazy instantiation pattern)
        self._get_by_id = GetByIdHandler(db_session, model_class)
        self._get_all = GetAllHandler(db_session, model_class)
        self._exists = ExistsHandler(db_session, model_class)
        self._count = CountHandler(db_session, model_class)
        self._create = CreateHandler(db_session)
        self._update = UpdateHandler(db_session)
        self._delete = DeleteHandler(db_session, model_class)
        self._find_paginated = FindPaginatedHandler(db_session, model_class)

    # Query use cases
    async def get_by_id(self, entity_id: Any) -> Optional[T]:
        """Query: Get entity by ID."""
        return await self._get_by_id.execute(entity_id)

    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Query: Get all entities."""
        return await self._get_all.execute(limit, offset)

    async def exists(self, entity_id: Any) -> bool:
        """Query: Check if entity exists."""
        return await self._exists.execute(entity_id)

    async def count(self) -> int:
        """Query: Count total entities."""
        return await self._count.execute()

    # Command use cases
    async def create(self, entity: T) -> T:
        """Command: Create new entity."""
        return await self._create.execute(entity)

    async def update(self, entity: T) -> T:
        """Command: Update existing entity."""
        return await self._update.execute(entity)

    async def delete(self, entity_id: Any) -> bool:
        """Command: Delete entity."""
        return await self._delete.execute(entity_id)

    # Pagination with Strategy Pattern
    async def find_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[List[FilterSpec]] = None,
        sort: Optional[List[SortSpec]] = None
    ) -> PaginatedResult[T]:
        """Query: Paginated results using Strategy Pattern."""
        return await self._find_paginated.execute(page, page_size, filters, sort)

    def get_pagination_backend_info(self) -> dict:
        """
        Get current pagination backend info (debugging/monitoring).

        Returns:
            dict: Backend metadata (FastCRUD or Native, availability)

        Example:
            >>> repo = UserRepository(session, UserORM)
            >>> info = repo.get_pagination_backend_info()
            >>> print(info["backend"])  # "FastCRUD" or "Native"
        """
        return self._find_paginated.get_backend_info()
