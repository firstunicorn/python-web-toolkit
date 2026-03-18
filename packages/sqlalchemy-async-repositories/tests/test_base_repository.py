"""Unit tests for BaseRepository implementation.

Tests BaseRepository with in-memory SQLite database.
RULE: Maximum 100 lines per file.
"""

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_async_repositories import BaseRepository


class Base(DeclarativeBase):
    """Base model for testing."""
    pass


class TestModel(Base):
    """Test model for repository testing."""
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
async def repository(db_session):
    """Create test repository."""
    return BaseRepository(db_session, TestModel)


async def test_repository_initialization(repository):
    """Should initialize repository with session and model."""
    assert repository.db is not None
    assert repository.model_class == TestModel


async def test_create_entity(repository, db_session):
    """Should create entity and return it with ID."""
    entity = TestModel(name="Test Item")
    result = await repository.create(entity)
    
    assert result.id is not None
    assert result.name == "Test Item"


async def test_get_by_id(repository, db_session):
    """Should retrieve entity by ID."""
    entity = TestModel(name="Get Test")
    created = await repository.create(entity)
    await db_session.commit()
    
    result = await repository.get_by_id(created.id)
    
    assert result is not None
    assert result.id == created.id
    assert result.name == "Get Test"


async def test_get_by_id_not_found(repository):
    """Should return None for non-existent ID."""
    result = await repository.get_by_id(999999)
    assert result is None


async def test_exists(repository, db_session):
    """Should check if entity exists."""
    entity = TestModel(name="Exists Test")
    created = await repository.create(entity)
    await db_session.commit()
    
    assert await repository.exists(created.id) is True
    assert await repository.exists(999999) is False


async def test_count(repository, db_session):
    """Should count entities."""
    initial_count = await repository.count()
    
    await repository.create(TestModel(name="Count1"))
    await repository.create(TestModel(name="Count2"))
    await db_session.commit()
    
    final_count = await repository.count()
    assert final_count == initial_count + 2
