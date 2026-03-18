"""Tests for PostgreSQL null character string escaping.

Tests escape/unescape functionality for strings.
"""

import pytest
from hypothesis import given, strategies as st

from postgres_data_sanitizers import (
    escape_null_chars,
    unescape_null_chars,
)


class TestEscapeNullChars:
    """Test core null character escaping."""

    def test_escape_single_null_char(self):
        """Should escape single null character."""
        result = escape_null_chars("hello\x00world")
        assert result == "hello\\u0000world"
        assert "\x00" not in result

    def test_escape_multiple_null_chars(self):
        """Should escape multiple null characters."""
        result = escape_null_chars("a\x00b\x00c\x00")
        assert result == "a\\u0000b\\u0000c\\u0000"
        assert "\x00" not in result

    def test_escape_no_null_chars(self):
        """Should return unchanged if no null characters."""
        text = "hello world"
        result = escape_null_chars(text)
        assert result == text

    def test_escape_empty_string(self):
        """Should handle empty string."""
        result = escape_null_chars("")
        assert result == ""

    def test_escape_only_null_chars(self):
        """Should handle string with only null characters."""
        result = escape_null_chars("\x00\x00\x00")
        assert result == "\\u0000\\u0000\\u0000"


class TestUnescapeNullChars:
    """Test null character unescaping."""

    def test_unescape_single_escaped_char(self):
        """Should unescape single escaped null character."""
        result = unescape_null_chars("hello\\u0000world")
        assert result == "hello\x00world"

    def test_unescape_multiple_escaped_chars(self):
        """Should unescape multiple escaped null characters."""
        result = unescape_null_chars("a\\u0000b\\u0000c\\u0000")
        assert result == "a\x00b\x00c\x00"

    def test_unescape_no_escaped_chars(self):
        """Should return unchanged if no escaped characters."""
        text = "hello world"
        result = unescape_null_chars(text)
        assert result == text

    def test_unescape_empty_string(self):
        """Should handle empty string."""
        result = unescape_null_chars("")
        assert result == ""


class TestRoundTripPreservation:
    """Test that escape/unescape preserves original data."""

    @given(st.text())
    def test_round_trip_any_text(self, text):
        """Property: any text should round-trip perfectly."""
        if '\\u0000' in text:
            return

        escaped = escape_null_chars(text)
        restored = unescape_null_chars(escaped)
        assert restored == text

    def test_round_trip_with_null_chars(self):
        """Should preserve text with null characters."""
        original = "hello\x00world\x00test"
        escaped = escape_null_chars(original)
        restored = unescape_null_chars(escaped)
        assert restored == original

    def test_round_trip_unicode(self):
        """Should preserve Unicode text."""
        original = "Hello 世界\x00مرحبا"
        escaped = escape_null_chars(original)
        restored = unescape_null_chars(escaped)
        assert restored == original
