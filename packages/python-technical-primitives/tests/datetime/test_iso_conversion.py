"""Property-based tests for ISO datetime conversion.

Tests ISO 8601 string conversion and UTC operations.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given
from datetime import timezone

from python_technical_primitives.datetime.operations import (
    utc_now,
    to_iso_string,
    from_iso_string,
)
from ..strategies.temporal import datetime_strategy


class TestISOConversion:
    """Property-based tests for ISO string conversion."""

    @given(dt=datetime_strategy())
    def test_iso_roundtrip(self, dt):
        """Converting to ISO and back should preserve datetime."""
        iso_str = to_iso_string(dt)
        result = from_iso_string(iso_str)
        assert result == dt

    @given(dt=datetime_strategy())
    def test_iso_string_format(self, dt):
        """ISO string should contain standard separators."""
        iso_str = to_iso_string(dt)
        assert 'T' in iso_str or ' ' in iso_str  # Date/time separator
        assert '-' in iso_str  # Date separator

    @given(dt=datetime_strategy())
    def test_iso_string_is_string(self, dt):
        """to_iso_string should return a string."""
        iso_str = to_iso_string(dt)
        assert isinstance(iso_str, str)
        assert len(iso_str) > 0

    @given(dt=datetime_strategy())
    def test_from_iso_returns_datetime(self, dt):
        """from_iso_string should return datetime object."""
        iso_str = to_iso_string(dt)
        result = from_iso_string(iso_str)
        from datetime import datetime
        assert isinstance(result, datetime)

    def test_iso_conversion_known_examples(self):
        """Test ISO conversion with known examples."""
        from datetime import datetime
        dt = datetime(2024, 1, 15, 10, 30, 45)
        iso_str = to_iso_string(dt)
        assert "2024" in iso_str
        assert "01" in iso_str
        assert "15" in iso_str

    @given(dt=datetime_strategy())
    def test_iso_conversion_is_idempotent(self, dt):
        """Converting to ISO twice should give same string."""
        iso1 = to_iso_string(dt)
        dt_back = from_iso_string(iso1)
        iso2 = to_iso_string(dt_back)
        assert iso1 == iso2


class TestUTCOperations:
    """Tests for UTC datetime operations."""

    def test_utc_now_has_timezone(self):
        """utc_now should return timezone-aware datetime."""
        result = utc_now()
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc

    def test_utc_now_returns_recent_time(self):
        """utc_now should return a datetime close to now."""
        from datetime import datetime, timedelta
        result = utc_now()
        now = datetime.now(timezone.utc)
        diff = abs((now - result).total_seconds())
        assert diff < 1.0  # Should be within 1 second

    def test_utc_now_increases_over_time(self):
        """Calling utc_now twice should give increasing times."""
        import time
        first = utc_now()
        time.sleep(0.01)  # Small delay
        second = utc_now()
        assert second >= first
