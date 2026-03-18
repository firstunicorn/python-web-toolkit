"""Property-based tests for Specification composition.

Tests AND, OR, NOT composition of specifications.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from .test_fixtures import (
    AlwaysTrueSpec,
    AlwaysFalseSpec,
    PositiveSpec,
    EvenSpec,
    OddSpec,
    RangeSpec,
)


class TestSpecificationComposition:
    """Property-based tests for specification composition."""

    @given(value=st.integers(min_value=1, max_value=100))
    def test_and_composition_both_must_pass(self, value):
        """AND composition requires both specs to pass."""
        spec = PositiveSpec() & EvenSpec()
        result = spec(value)
        assert result == (value > 0 and value % 2 == 0)

    @given(value=st.integers(min_value=-100, max_value=100))
    def test_or_composition_one_must_pass(self, value):
        """OR composition requires at least one spec to pass."""
        spec = PositiveSpec() | EvenSpec()
        result = spec(value)
        assert result == (value > 0 or value % 2 == 0)

    @given(value=st.integers())
    def test_not_composition_inverts(self, value):
        """NOT composition inverts the result."""
        spec = ~PositiveSpec()
        result = spec(value)
        assert result == (value <= 0)

    @given(value=st.integers())
    def test_complex_composition(self, value):
        """Complex compositions work correctly."""
        # (positive AND even) OR (NOT positive)
        spec = (PositiveSpec() & EvenSpec()) | ~PositiveSpec()
        result = spec(value)
        expected = (value > 0 and value % 2 == 0) or (value <= 0)
        assert result == expected

    @given(value=st.integers())
    def test_and_with_always_false(self, value):
        """AND with AlwaysFalse should always be False."""
        spec = PositiveSpec() & AlwaysFalseSpec()
        assert spec(value) is False

    @given(value=st.integers())
    def test_or_with_always_true(self, value):
        """OR with AlwaysTrue should always be True."""
        spec = PositiveSpec() | AlwaysTrueSpec()
        assert spec(value) is True

    @given(value=st.integers())
    def test_double_negation(self, value):
        """Double negation should equal original."""
        spec = PositiveSpec()
        double_neg = ~~spec
        assert double_neg(value) == spec(value)

    @given(value=st.integers())
    def test_and_composition_is_commutative(self, value):
        """AND composition should be commutative: a & b == b & a."""
        spec1 = PositiveSpec() & EvenSpec()
        spec2 = EvenSpec() & PositiveSpec()
        assert spec1(value) == spec2(value)

    @given(value=st.integers())
    def test_or_composition_is_commutative(self, value):
        """OR composition should be commutative: a | b == b | a."""
        spec1 = PositiveSpec() | OddSpec()
        spec2 = OddSpec() | PositiveSpec()
        assert spec1(value) == spec2(value)

    @given(value=st.integers())
    def test_de_morgans_law(self, value):
        """De Morgan's law: NOT (a AND b) == (NOT a) OR (NOT b)."""
        spec1 = ~(PositiveSpec() & EvenSpec())
        spec2 = ~PositiveSpec() | ~EvenSpec()
        assert spec1(value) == spec2(value)
