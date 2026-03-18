"""Unit tests for field transformation utilities.

Tests string case conversions and datetime mapping functions.
RULE: Maximum 100 lines per file.
"""

import pytest
from datetime import datetime
from python_dto_mappers import (
    to_upper,
    to_lower,
    to_sentence_case,
    to_title_case,
    map_datetime_to_iso,
    map_iso_to_datetime,
)


def test_to_upper():
    """Should convert text to uppercase."""
    assert to_upper("hello") == "HELLO"
    assert to_upper("Hello World") == "HELLO WORLD"
    assert to_upper("123abc") == "123ABC"


def test_to_lower():
    """Should convert text to lowercase."""
    assert to_lower("HELLO") == "hello"
    assert to_lower("Hello World") == "hello world"
    assert to_lower("123ABC") == "123abc"


def test_to_sentence_case():
    """Should capitalize first letter only."""
    assert to_sentence_case("hello world") == "Hello world"
    assert to_sentence_case("HELLO") == "Hello"
    assert to_sentence_case("") == ""


def test_to_title_case():
    """Should capitalize each word."""
    assert to_title_case("hello world") == "Hello World"
    assert to_title_case("the quick brown fox") == "The Quick Brown Fox"
    assert to_title_case("api response") == "Api Response"


def test_map_datetime_to_iso_with_datetime():
    """Should convert datetime to ISO string."""
    dt = datetime(2024, 1, 15, 10, 30, 45)
    result = map_datetime_to_iso(dt)
    assert result == "2024-01-15T10:30:45"


def test_map_datetime_to_iso_with_none():
    """Should return None for None input."""
    assert map_datetime_to_iso(None) is None


def test_map_iso_to_datetime_with_string():
    """Should convert ISO string to datetime."""
    result = map_iso_to_datetime("2024-01-15T10:30:45")
    assert result == datetime(2024, 1, 15, 10, 30, 45)


def test_map_iso_to_datetime_with_none():
    """Should return None for None input."""
    assert map_iso_to_datetime(None) is None


def test_map_iso_to_datetime_with_timezone():
    """Should handle ISO strings with timezone."""
    result = map_iso_to_datetime("2024-01-15T10:30:45+00:00")
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_datetime_roundtrip():
    """Should maintain value through ISO conversion roundtrip."""
    original = datetime(2024, 6, 15, 14, 30, 0)
    iso_str = map_datetime_to_iso(original)
    result = map_iso_to_datetime(iso_str)
    assert result == original
