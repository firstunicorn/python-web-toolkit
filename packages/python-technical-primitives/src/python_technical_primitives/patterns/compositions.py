"""
Specification composition classes (AND, OR, NOT).
Part of DIY Specification pattern.
"""
from typing import TypeVar
from .base import Specification

T = TypeVar('T')


class AndSpecification(Specification[T]):
    """AND composition: both must be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]):
        super().__init__()
        self.left = left
        self.right = right
        self.description = f"({left.description}) AND ({right.description})"

    def is_satisfied_by(self, candidate: T) -> bool:
        self._errors.clear()
        left_result = self.left.is_satisfied_by(candidate)
        right_result = self.right.is_satisfied_by(candidate)
        if not left_result:
            self._errors.update(self.left.errors)
        if not right_result:
            self._errors.update(self.right.errors)
        return left_result and right_result


class OrSpecification(Specification[T]):
    """OR composition: at least one must be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]):
        super().__init__()
        self.left = left
        self.right = right
        self.description = f"({left.description}) OR ({right.description})"

    def is_satisfied_by(self, candidate: T) -> bool:
        self._errors.clear()
        left_result = self.left.is_satisfied_by(candidate)
        if left_result:
            return True
        right_result = self.right.is_satisfied_by(candidate)
        if right_result:
            return True
        self._errors.update(self.left.errors)
        self._errors.update(self.right.errors)
        return False


class NotSpecification(Specification[T]):
    """NOT composition: must NOT be satisfied."""

    def __init__(self, spec: Specification[T]):
        super().__init__()
        self.spec = spec
        self.description = f"NOT ({spec.description})"

    def is_satisfied_by(self, candidate: T) -> bool:
        self._errors.clear()
        result = self.spec.is_satisfied_by(candidate)
        if result:
            self._errors[type(self.spec).__name__] = (
                f"Expected NOT to satisfy: {self.spec.description}"
            )
        return not result






