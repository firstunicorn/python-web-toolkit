"""Property-based tests for text truncation and whitespace.

Tests truncation and whitespace normalization functions.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_technical_primitives.text.operations import (
    truncate,
    normalize_whitespace,
)
from ..strategies.text import (
    safe_ascii_text_strategy,
    whitespace_text_strategy,
)


class TestTruncation:
    """Property-based tests for truncation."""

    @given(text=safe_ascii_text_strategy(), max_len=st.integers(min_value=4, max_value=50))
    def test_truncate_respects_max_length(self, text, max_len):
        """Truncated text should not exceed max_length."""
        result = truncate(text, max_len)
        assert len(result) <= max_len

    @given(text=st.text(max_size=10))
    def test_short_text_not_truncated(self, text):
        """Text shorter than max_length should not be truncated."""
        result = truncate(text, 100)
        assert result == text

    @given(text=st.text(min_size=20, max_size=50))
    def test_truncate_adds_suffix(self, text):
        """Truncated text should end with suffix."""
        result = truncate(text, 10)
        if len(text) > 10:
            assert result.endswith("...")

    def test_truncate_with_custom_suffix(self):
        """Truncate should support custom suffix."""
        result = truncate("Hello World", 8, suffix="…")
        assert len(result) <= 8
        assert result.endswith("…")

    @given(text=safe_ascii_text_strategy())
    def test_truncate_preserves_short_text(self, text):
        """Text at or below max_length should be preserved."""
        if len(text) <= 50:
            result = truncate(text, 50)
            assert result == text


class TestWhitespace:
    """Property-based tests for whitespace normalization."""

    @given(text=whitespace_text_strategy())
    def test_normalize_removes_extra_whitespace(self, text):
        """normalize_whitespace should collapse multiple spaces."""
        result = normalize_whitespace(text)
        assert '  ' not in result  # No double spaces

    @given(text=safe_ascii_text_strategy())
    def test_normalize_is_idempotent(self, text):
        """Normalizing twice should give same result."""
        first = normalize_whitespace(text)
        second = normalize_whitespace(first)
        assert first == second

    def test_normalize_handles_multiple_whitespace_types(self):
        """Normalize should handle tabs, newlines, etc."""
        text = "hello\t\tworld\n\ntest"
        result = normalize_whitespace(text)
        assert result == "hello world test"

    def test_normalize_strips_leading_trailing(self):
        """Normalize should strip leading/trailing whitespace."""
        result = normalize_whitespace("  hello  ")
        assert result == "hello"

    @given(text=st.text(min_size=1, max_size=50))
    def test_normalize_never_returns_only_whitespace(self, text):
        """Normalized text should not be only whitespace."""
        result = normalize_whitespace(text)
        if result:  # If not empty
            assert result.strip() == result
