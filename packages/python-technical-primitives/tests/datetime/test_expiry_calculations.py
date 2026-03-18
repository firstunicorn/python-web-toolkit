"""Property-based tests for expiry calculations.

Tests expiry checking and days_until calculation.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st
from datetime import timedelta

from python_technical_primitives.datetime.operations import (
    is_expired,
    days_until,
)
from ..strategies.temporal import (
    datetime_strategy,
    future_datetime_strategy,
    past_datetime_strategy,
)


class TestExpiryChecks:
    """Property-based tests for expiry checking."""

    @given(expiry_dt=past_datetime_strategy())
    def test_past_datetime_is_expired(self, expiry_dt):
        """Past datetime should be expired."""
        assert is_expired(expiry_dt)

    @given(expiry_dt=future_datetime_strategy())
    def test_future_datetime_not_expired(self, expiry_dt):
        """Future datetime should not be expired."""
        assert not is_expired(expiry_dt)

    @given(dt=datetime_strategy())
    def test_expired_with_same_reference(self, dt):
        """Datetime is expired when reference is same datetime."""
        assert is_expired(dt, reference_dt=dt)

    @given(dt=datetime_strategy(), hours=st.integers(min_value=1, max_value=100))
    def test_expired_with_future_reference(self, dt, hours):
        """Datetime is expired when reference is in future."""
        future_ref = dt + timedelta(hours=hours)
        assert is_expired(dt, reference_dt=future_ref)

    @given(dt=datetime_strategy(), hours=st.integers(min_value=1, max_value=100))
    def test_not_expired_with_past_reference(self, dt, hours):
        """Datetime is not expired when reference is in past."""
        past_ref = dt - timedelta(hours=hours)
        assert not is_expired(dt, reference_dt=past_ref)


class TestDaysUntil:
    """Property-based tests for days_until calculation."""

    @given(target=future_datetime_strategy())
    def test_future_datetime_positive_days(self, target):
        """days_until future datetime should be positive."""
        result = days_until(target)
        assert result >= 0

    @given(target=past_datetime_strategy())
    def test_past_datetime_negative_days(self, target):
        """days_until past datetime should be negative."""
        result = days_until(target)
        assert result <= 0

    @given(dt=datetime_strategy())
    def test_days_until_same_datetime(self, dt):
        """days_until same datetime should be 0."""
        result = days_until(dt, reference_dt=dt)
        assert result == 0

    @given(dt=datetime_strategy(), days=st.integers(min_value=1, max_value=100))
    def test_days_until_matches_days_added(self, dt, days):
        """days_until should match number of days added."""
        target = dt + timedelta(days=days)
        result = days_until(target, reference_dt=dt)
        assert result == days

    @given(dt=datetime_strategy(), days=st.integers(min_value=1, max_value=100))
    def test_days_until_negative_for_past(self, dt, days):
        """days_until past datetime should be negative."""
        target = dt - timedelta(days=days)
        result = days_until(target, reference_dt=dt)
        assert result == -days

    @given(ref=datetime_strategy(), days_diff=st.integers(min_value=1, max_value=100))
    def test_days_until_symmetric_full_days(self, ref, days_diff):
        """days_until should be symmetric for exact day differences."""
        from datetime import timedelta
        target = ref + timedelta(days=days_diff)
        
        forward = days_until(target, reference_dt=ref)
        backward = days_until(ref, reference_dt=target)
        # With exact day differences, symmetry holds
        assert forward == -backward
        assert forward == days_diff
