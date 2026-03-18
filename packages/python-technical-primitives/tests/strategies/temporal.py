"""Temporal (datetime) generation strategies.

Property-based datetime generation for testing time-based logic.
RULE: Maximum 100 lines per file.
"""

from hypothesis import strategies as st
from datetime import datetime, timedelta, timezone


@st.composite
def datetime_strategy(draw, min_year=2020, max_year=2030):
    """Generate datetime objects within a reasonable range.
    
    Configurable year bounds for different test scenarios.
    """
    return draw(st.datetimes(
        min_value=datetime(min_year, 1, 1),
        max_value=datetime(max_year, 12, 31)
    ))


@st.composite
def future_datetime_strategy(draw, min_hours=1, max_hours=8760):
    """Generate future datetime objects.
    
    Args:
        min_hours: Minimum hours from now (default: 1)
        max_hours: Maximum hours from now (default: 8760 = 1 year)
    """
    hours = draw(st.integers(min_value=min_hours, max_value=max_hours))
    return datetime.now(timezone.utc) + timedelta(hours=hours)


@st.composite
def past_datetime_strategy(draw, min_hours=1, max_hours=8760):
    """Generate past datetime objects.
    
    Args:
        min_hours: Minimum hours ago (default: 1)
        max_hours: Maximum hours ago (default: 8760 = 1 year)
    """
    hours = draw(st.integers(min_value=min_hours, max_value=max_hours))
    return datetime.now(timezone.utc) - timedelta(hours=hours)


@st.composite
def timedelta_strategy(draw, min_seconds=0, max_seconds=86400):
    """Generate timedelta objects.
    
    Args:
        min_seconds: Minimum seconds (default: 0)
        max_seconds: Maximum seconds (default: 86400 = 1 day)
    """
    seconds = draw(st.integers(min_value=min_seconds, max_value=max_seconds))
    return timedelta(seconds=seconds)

