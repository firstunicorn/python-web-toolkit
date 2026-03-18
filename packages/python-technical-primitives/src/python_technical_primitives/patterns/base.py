"""
Base Specification class for DIY Specification pattern.
No external dependencies - we own this code.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .compositions import AndSpecification, OrSpecification, NotSpecification

T = TypeVar('T')


class Specification(ABC, Generic[T]):
    """
    Base class for all specifications.
    Supports boolean composition (&, |, ~) and error tracking.

    Example:
        >>> class AdultSpec(Specification[User]):
        ...     description = "User must be 18+"
        ...     def is_satisfied_by(self, user):
        ...         return user.age >= 18
        >>>
        >>> spec = AdultSpec() & VerifiedEmailSpec()
        >>> if spec(user):
        ...     process_user(user)
    """

    description: str = "No description provided."

    def __init__(self):
        self._errors: Dict[str, str] = {}

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies specification."""
        pass

    def __call__(self, candidate: T) -> bool:
        """Allow calling spec directly: spec(candidate)"""
        return self.is_satisfied_by(candidate)

    @property
    def errors(self) -> Dict[str, str]:
        """Get errors from last validation."""
        return self._errors

    def _add_error(self) -> None:
        """Helper: add this spec's error."""
        self._errors[self.__class__.__name__] = self.description

    def __and__(self, other: 'Specification[T]') -> 'AndSpecification[T]':
        """Combine with AND: spec1 & spec2"""
        from .compositions import AndSpecification
        return AndSpecification(self, other)

    def __or__(self, other: 'Specification[T]') -> 'OrSpecification[T]':
        """Combine with OR: spec1 | spec2"""
        from .compositions import OrSpecification
        return OrSpecification(self, other)

    def __invert__(self) -> 'NotSpecification[T]':
        """Negate with NOT: ~spec"""
        from .compositions import NotSpecification
        return NotSpecification(self)






