"""Repository interface definitions."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Any

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Base repository interface for common database operations."""

    @abstractmethod
    async def get_by_id(self, entity_id: Any) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update existing entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: Any) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Get all entities with optional pagination."""
        pass

    @abstractmethod
    async def exists(self, entity_id: Any) -> bool:
        """Check if entity exists by ID."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Get total count of entities."""
        pass






