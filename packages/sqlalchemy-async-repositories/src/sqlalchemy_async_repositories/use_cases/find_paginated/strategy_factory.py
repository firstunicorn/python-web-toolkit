"""
Strategy Factory for pagination backends.

Design Pattern: Factory Pattern
Purpose: Creates appropriate pagination strategy based on available dependencies.

Why Factory Pattern?
- Encapsulates object creation logic
- Single responsibility (SRP)
- Easy to test and mock
- Centralizes strategy selection
"""

from ...pagination.models import has_fastcrud
from ...pagination.strategies import IPaginationStrategy, NativeStrategy

try:
    from ...pagination.strategies import FastCRUDStrategy
    _FASTCRUD_AVAILABLE = True
except ImportError:
    FastCRUDStrategy = None  # type: ignore
    _FASTCRUD_AVAILABLE = False


class PaginationStrategyFactory:
    """
    Factory for creating pagination strategy instances.

    Implements Factory Pattern to abstract strategy instantiation.

    Selection Logic:
    1. FastCRUD available → FastCRUDStrategy (battle-tested, feature-rich)
    2. Fallback → NativeStrategy (zero dependencies, simple)

    Example:
        >>> factory = PaginationStrategyFactory()
        >>> strategy = factory.create()
        >>> backend = factory.get_backend_name(strategy)
        >>> print(backend)  # "FastCRUD" or "Native"
    """

    @staticmethod
    def create() -> IPaginationStrategy:
        """
        Create appropriate pagination strategy (Factory Method).

        Returns:
            IPaginationStrategy: Strategy instance (FastCRUD or Native)
        """
        if has_fastcrud() and FastCRUDStrategy is not None:
            return FastCRUDStrategy()
        return NativeStrategy()

    @staticmethod
    def get_backend_name(strategy: IPaginationStrategy) -> str:
        """
        Get human-readable backend name from strategy instance.

        Args:
            strategy: Strategy instance

        Returns:
            str: "FastCRUD" or "Native"
        """
        class_name = strategy.__class__.__name__
        return "FastCRUD" if "FastCRUD" in class_name else "Native"

    @staticmethod
    def is_fastcrud_available() -> bool:
        """
        Check if FastCRUD is available for use.

        Returns:
            bool: True if FastCRUD can be used, False otherwise
        """
        return has_fastcrud()


