"""Test fixtures for Specification pattern tests.

Shared test specification classes used across pattern tests.
RULE: Maximum 100 lines per file.
"""

from python_technical_primitives.patterns.base import Specification


class AlwaysTrueSpec(Specification[int]):
    """Specification that always returns True."""
    description = "Always true specification"

    def is_satisfied_by(self, candidate: int) -> bool:
        return True


class AlwaysFalseSpec(Specification[int]):
    """Specification that always returns False."""
    description = "Always false specification"

    def is_satisfied_by(self, candidate: int) -> bool:
        return False


class PositiveSpec(Specification[int]):
    """Specification for positive numbers."""
    description = "Number must be positive"

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > 0


class EvenSpec(Specification[int]):
    """Specification for even numbers."""
    description = "Number must be even"

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 == 0


class OddSpec(Specification[int]):
    """Specification for odd numbers."""
    description = "Number must be odd"

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 != 0


class RangeSpec(Specification[int]):
    """Specification for numbers within a range."""
    description = "Number must be within range"

    def __init__(self, min_value: int, max_value: int):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def is_satisfied_by(self, candidate: int) -> bool:
        return self.min_value <= candidate <= self.max_value
