"""Unit tests for IRepository interface contract.

Tests that the repository interface defines correct contracts.
RULE: Maximum 100 lines per file.
"""

import pytest
from typing import Optional, List, Any
from sqlalchemy_async_repositories import IRepository


class ConcreteRepository(IRepository[dict]):
    """Concrete implementation for testing interface contract."""
    
    async def get_by_id(self, entity_id: Any) -> Optional[dict]:
        return {"id": entity_id}
    
    async def create(self, entity: dict) -> dict:
        return {**entity, "id": 1}
    
    async def update(self, entity: dict) -> dict:
        return entity
    
    async def delete(self, entity_id: Any) -> bool:
        return True
    
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[dict]:
        return [{"id": 1}, {"id": 2}]
    
    async def exists(self, entity_id: Any) -> bool:
        return True
    
    async def count(self) -> int:
        return 10


async def test_repository_implements_get_by_id():
    """Should implement get_by_id method."""
    repo = ConcreteRepository()
    result = await repo.get_by_id(1)
    assert result == {"id": 1}


async def test_repository_implements_create():
    """Should implement create method."""
    repo = ConcreteRepository()
    entity = {"name": "test"}
    result = await repo.create(entity)
    assert result["id"] == 1
    assert result["name"] == "test"


async def test_repository_implements_update():
    """Should implement update method."""
    repo = ConcreteRepository()
    entity = {"id": 1, "name": "updated"}
    result = await repo.update(entity)
    assert result == entity


async def test_repository_implements_delete():
    """Should implement delete method."""
    repo = ConcreteRepository()
    result = await repo.delete(1)
    assert result is True


async def test_repository_implements_get_all():
    """Should implement get_all method."""
    repo = ConcreteRepository()
    result = await repo.get_all()
    assert len(result) == 2


async def test_repository_implements_exists():
    """Should implement exists method."""
    repo = ConcreteRepository()
    result = await repo.exists(1)
    assert result is True


async def test_repository_implements_count():
    """Should implement count method."""
    repo = ConcreteRepository()
    result = await repo.count()
    assert result == 10


async def test_repository_get_all_with_pagination():
    """Should support pagination parameters."""
    repo = ConcreteRepository()
    result = await repo.get_all(limit=10, offset=5)
    assert isinstance(result, list)
