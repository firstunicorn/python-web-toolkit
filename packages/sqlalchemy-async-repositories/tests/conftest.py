"""Shared test fixtures for sqlalchemy-async-repositories.

Uses Testcontainers for real PostgreSQL database in tests.
RULE: Maximum 100 lines per file.
"""

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from testcontainers.postgres import PostgresContainer


class Base(DeclarativeBase):
    """Base model for testing."""
    pass


class SampleModel(Base):
    """Test model for repository and pagination testing."""
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(Integer, nullable=True)


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for the test session."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture
async def db_session(postgres_container):
    """Create async database session with test schema."""
    connection_url = postgres_container.get_connection_url().replace(
        "psycopg2", "asyncpg"
    )
    
    engine = create_async_engine(connection_url, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
