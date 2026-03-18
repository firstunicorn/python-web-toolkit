"""Property-based tests for base Specification pattern.

Tests the Specification base class functionality.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_technical_primitives.patterns.base import Specification
from .test_fixtures import AlwaysTrueSpec, AlwaysFalseSpec, PositiveSpec, EvenSpec


class TestSpecificationBasics:
    """Property-based tests for base Specification."""

    @given(value=st.integers())
    def test_spec_can_be_called_directly(self, value):
        """Specification can be called as function."""
        spec = AlwaysTrueSpec()
        assert spec(value) == spec.is_satisfied_by(value)

    @given(value=st.integers())
    def test_always_true_spec_property(self, value):
        """AlwaysTrueSpec should always return True."""
        spec = AlwaysTrueSpec()
        assert spec(value) is True

    @given(value=st.integers())
    def test_always_false_spec_property(self, value):
        """AlwaysFalseSpec should always return False."""
        spec = AlwaysFalseSpec()
        assert spec(value) is False

    @given(value=st.integers(min_value=1))
    def test_positive_spec_for_positive_numbers(self, value):
        """PositiveSpec should return True for positive numbers."""
        spec = PositiveSpec()
        assert spec(value) is True

    @given(value=st.integers(max_value=0))
    def test_positive_spec_for_non_positive_numbers(self, value):
        """PositiveSpec should return False for non-positive numbers."""
        spec = PositiveSpec()
        assert spec(value) is False

    @given(value=st.integers())
    def test_even_spec_property(self, value):
        """EvenSpec should match modulo 2 check."""
        spec = EvenSpec()
        assert spec(value) == (value % 2 == 0)

    def test_spec_has_description(self):
        """Specification should have description attribute."""
        spec = PositiveSpec()
        assert hasattr(spec, 'description')
        assert isinstance(spec.description, str)
        assert len(spec.description) > 0

    def test_spec_has_errors_property(self):
        """Specification should have errors property."""
        spec = PositiveSpec()
        assert hasattr(spec, 'errors')
        assert isinstance(spec.errors, dict)

    @given(value=st.integers())
    def test_spec_callable_interface(self, value):
        """Specification should be callable."""
        spec = PositiveSpec()
        result = spec(value)
        assert isinstance(result, bool)

    @given(value1=st.integers(), value2=st.integers())
    def test_spec_stateless_behavior(self, value1, value2):
        """Calling spec multiple times should be stateless."""
        spec = PositiveSpec()
        result1 = spec(value1)
        result2 = spec(value2)
        # Calling with value2 shouldn't affect value1's result
        result1_again = spec(value1)
        assert result1 == result1_again
