"""Specification pattern utilities."""

from .base import Specification
from .compositions import AndSpecification, OrSpecification, NotSpecification

__all__ = [
    "Specification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]






