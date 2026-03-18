"""Property-based tests for text case conversion.

Tests case conversion functions with various inputs.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given

from python_technical_primitives.text.operations import (
    to_sentence_case,
    to_lower_case,
    to_upper_case,
)
from ..strategies.text import (
    any_text_input_strategy,
    mixed_case_text_strategy,
)


class TestCaseConversion:
    """Property-based tests for case conversion functions."""

    @given(text=any_text_input_strategy())
    def test_to_lower_case_property(self, text):
        """to_lower_case should always return lowercase."""
        result = to_lower_case(text)
        assert result == result.lower()

    @given(text=any_text_input_strategy())
    def test_to_upper_case_property(self, text):
        """to_upper_case should always return uppercase."""
        result = to_upper_case(text)
        assert result == result.upper()

    def test_sentence_case_basic_behavior(self):
        """to_sentence_case should capitalize first letter for ASCII."""
        # Test with ASCII letters where uppercase is well-defined
        assert to_sentence_case("hello")[0] == "H"
        assert to_sentence_case("world")[0] == "W"
        
        # Test with already capitalized
        result = to_sentence_case("Hello")
        assert result == "Hello"

    def test_empty_string_remains_empty(self):
        """Empty string should remain empty for all conversions."""
        assert to_sentence_case("") == ""
        assert to_lower_case("") == ""
        assert to_upper_case("") == ""

    def test_sentence_case_basic_examples(self):
        """Test sentence case with known examples."""
        assert to_sentence_case("hello") == "Hello"
        assert to_sentence_case("WORLD") == "World"
        assert to_sentence_case("HeLLo WoRLd") == "Hello world"

    @given(text=any_text_input_strategy())
    def test_case_conversion_idempotent(self, text):
        """Converting case twice should give same result."""
        lower_once = to_lower_case(text)
        lower_twice = to_lower_case(lower_once)
        assert lower_once == lower_twice

        upper_once = to_upper_case(text)
        upper_twice = to_upper_case(upper_once)
        assert upper_once == upper_twice
