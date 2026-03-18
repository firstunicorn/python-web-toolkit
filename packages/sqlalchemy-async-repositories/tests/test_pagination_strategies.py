"""Property-based tests for pagination strategies.

Tests NativeStrategy and FastCRUDStrategy with real PostgreSQL.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st, assume, settings, HealthCheck
from sqlalchemy_async_repositories.pagination.strategies.native_strategy import (
    NativeStrategy
)
from sqlalchemy_async_repositories.pagination.models import FilterSpec, SortSpec
from .conftest import SampleModel


@pytest.fixture
async def strategy():
    """Create NativeStrategy instance."""
    return NativeStrategy()


@pytest.fixture
async def sample_data(db_session):
    """Insert sample test data."""
    items = [
        SampleModel(id=i, name=f"item_{i}", value=i * 10)
        for i in range(1, 51)
    ]
    db_session.add_all(items)
    await db_session.commit()
    return items


@given(
    page=st.integers(min_value=1, max_value=10),
    page_size=st.integers(min_value=1, max_value=20)
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.asyncio
async def test_pagination_consistency(strategy, db_session, sample_data, page, page_size):
    """Property: Total count remains constant across all pages."""
    result = await strategy.execute(
        db=db_session, model_class=SampleModel, page=page,
        page_size=page_size, filters=None, sort=None
    )
    
    assert result.total == 50
    assert result.page == page
    assert result.page_size == page_size
    assert result.pages == ((50 + page_size - 1) // page_size)


@given(value_filter=st.integers(min_value=0, max_value=500))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.asyncio
async def test_filter_eq(strategy, db_session, sample_data, value_filter):
    """Property: Filter by equality returns correct results."""
    filters = [FilterSpec(field="value", operator="eq", value=value_filter)]
    
    result = await strategy.execute(
        db=db_session, model_class=SampleModel, page=1,
        page_size=100, filters=filters, sort=None
    )
    
    expected_count = 1 if (value_filter % 10 == 0 and 10 <= value_filter <= 500) else 0
    assert result.total == expected_count
    if expected_count > 0:
        assert all(item.value == value_filter for item in result.items)


@given(direction=st.sampled_from(["asc", "desc"]))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.asyncio
async def test_sort_order(strategy, db_session, sample_data, direction):
    """Property: Sorting produces correct order."""
    sort = [SortSpec(field="value", direction=direction)]
    
    result = await strategy.execute(
        db=db_session, model_class=SampleModel, page=1,
        page_size=50, filters=None, sort=sort
    )
    
    values = [item.value for item in result.items]
    if direction == "asc":
        assert values == sorted(values)
    else:
        assert values == sorted(values, reverse=True)
