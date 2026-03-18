"""Property-based tests for datetime manipulation.

Tests datetime addition and manipulation functions.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st
from datetime import timedelta

from python_technical_primitives.datetime.operations import (
    add_days,
    add_hours,
)
from ..strategies.temporal import datetime_strategy


class TestDatetimeAddition:
    """Property-based tests for datetime addition functions."""

    @given(dt=datetime_strategy(), days=st.integers(min_value=-365, max_value=365))
    def test_add_days_property(self, dt, days):
        """add_days should add exactly N days."""
        result = add_days(dt, days)
        expected = dt + timedelta(days=days)
        assert result == expected

    @given(dt=datetime_strategy(), hours=st.integers(min_value=-100, max_value=100))
    def test_add_hours_property(self, dt, hours):
        """add_hours should add exactly N hours."""
        result = add_hours(dt, hours)
        expected = dt + timedelta(hours=hours)
        assert result == expected

    @given(dt=datetime_strategy())
    def test_add_zero_returns_same_datetime(self, dt):
        """Adding zero days/hours should return same datetime."""
        assert add_days(dt, 0) == dt
        assert add_hours(dt, 0) == dt

    @given(dt=datetime_strategy())
    def test_add_positive_increases_datetime(self, dt):
        """Adding positive values should increase datetime."""
        later_day = add_days(dt, 1)
        later_hour = add_hours(dt, 1)
        assert later_day > dt
        assert later_hour > dt

    @given(dt=datetime_strategy())
    def test_add_negative_decreases_datetime(self, dt):
        """Adding negative values should decrease datetime."""
        earlier_day = add_days(dt, -1)
        earlier_hour = add_hours(dt, -1)
        assert earlier_day < dt
        assert earlier_hour < dt

    @given(dt=datetime_strategy(), days=st.integers(min_value=1, max_value=100))
    def test_add_days_is_reversible(self, dt, days):
        """Adding then subtracting days should return original."""
        later = add_days(dt, days)
        back = add_days(later, -days)
        assert back == dt

    @given(dt=datetime_strategy(), hours=st.integers(min_value=1, max_value=100))
    def test_add_hours_is_reversible(self, dt, hours):
        """Adding then subtracting hours should return original."""
        later = add_hours(dt, hours)
        back = add_hours(later, -hours)
        assert back == dt

    @given(dt=datetime_strategy())
    def test_add_24_hours_equals_1_day(self, dt):
        """Adding 24 hours should equal adding 1 day."""
        by_hours = add_hours(dt, 24)
        by_days = add_days(dt, 1)
        assert by_hours == by_days

    @given(dt=datetime_strategy(), days1=st.integers(-50, 50), days2=st.integers(-50, 50))
    def test_add_days_is_associative(self, dt, days1, days2):
        """add_days should be associative: (dt + a) + b == dt + (a + b)."""
        result1 = add_days(add_days(dt, days1), days2)
        result2 = add_days(dt, days1 + days2)
        assert result1 == result2
