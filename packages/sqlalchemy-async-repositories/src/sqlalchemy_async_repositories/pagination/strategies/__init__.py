"""Pagination strategies (Strategy Pattern)."""

from .base import IPaginationStrategy
from .native_strategy import NativeStrategy

try:
    from .fastcrud_strategy import FastCRUDStrategy
    __all__ = ["IPaginationStrategy", "NativeStrategy", "FastCRUDStrategy"]
except ImportError:
    __all__ = ["IPaginationStrategy", "NativeStrategy"]

