"""Tests for PostgreSQL dict sanitization.

Tests sanitize/unescape functionality for dictionaries.
"""

import pytest

from postgres_data_sanitizers import (
    sanitize_dict_for_postgres,
    unescape_dict_from_postgres,
)


class TestSanitizeDictForPostgres:
    """Test dictionary sanitization."""

    def test_sanitize_simple_dict(self):
        """Should escape null chars in simple dict."""
        data = {"key": "value\x00"}
        result = sanitize_dict_for_postgres(data)
        assert result == {"key": "value\\u0000"}

    def test_sanitize_dict_with_null_in_key(self):
        """Should escape null chars in dict keys."""
        data = {"key\x00": "value"}
        result = sanitize_dict_for_postgres(data)
        assert result == {"key\\u0000": "value"}

    def test_sanitize_nested_dict(self):
        """Should recursively sanitize nested dicts."""
        data = {
            "outer": "val\x00",
            "nested": {
                "inner\x00": "data\x00"
            }
        }
        result = sanitize_dict_for_postgres(data)
        assert result == {
            "outer": "val\\u0000",
            "nested": {
                "inner\\u0000": "data\\u0000"
            }
        }

    def test_sanitize_dict_with_list(self):
        """Should sanitize strings in lists."""
        data = {
            "items": ["a\x00", "b", "c\x00"]
        }
        result = sanitize_dict_for_postgres(data)
        assert result == {
            "items": ["a\\u0000", "b", "c\\u0000"]
        }

    def test_sanitize_dict_with_nested_list_of_dicts(self):
        """Should sanitize nested lists of dicts."""
        data = {
            "items": [
                {"key\x00": "val\x00"},
                {"normal": "value"}
            ]
        }
        result = sanitize_dict_for_postgres(data)
        assert result == {
            "items": [
                {"key\\u0000": "val\\u0000"},
                {"normal": "value"}
            ]
        }

    def test_sanitize_dict_preserves_non_string_types(self):
        """Should preserve non-string types."""
        data = {
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3]
        }
        result = sanitize_dict_for_postgres(data)
        assert result == data

    def test_sanitize_non_dict_returns_as_is(self):
        """Should return non-dict types unchanged."""
        assert sanitize_dict_for_postgres("string") == "string"
        assert sanitize_dict_for_postgres(42) == 42
        assert sanitize_dict_for_postgres(None) is None


class TestUnescapeDictFromPostgres:
    """Test dictionary unescaping."""

    def test_unescape_simple_dict(self):
        """Should unescape null chars in simple dict."""
        data = {"key": "value\\u0000"}
        result = unescape_dict_from_postgres(data)
        assert result == {"key": "value\x00"}

    def test_unescape_nested_dict(self):
        """Should recursively unescape nested dicts."""
        data = {
            "outer": "val\\u0000",
            "nested": {"inner\\u0000": "data\\u0000"}
        }
        result = unescape_dict_from_postgres(data)
        assert result == {
            "outer": "val\x00",
            "nested": {"inner\x00": "data\x00"}
        }

    def test_dict_round_trip(self):
        """Should preserve dict through sanitize/unescape cycle."""
        original = {
            "user\x00": "John\x00Doe",
            "metadata": {"tags\x00": ["tag1\x00", "tag2"]},
            "count": 42
        }
        sanitized = sanitize_dict_for_postgres(original)
        restored = unescape_dict_from_postgres(sanitized)
        assert restored == original
