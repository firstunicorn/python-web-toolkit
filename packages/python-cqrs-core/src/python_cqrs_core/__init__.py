"""Python CQRS Core - CQRS interfaces and base classes."""

from python_cqrs_core.command import ICommand, ICommandHandler
from python_cqrs_core.query import IQuery, IQueryHandler
from python_cqrs_core.base_command import BaseCommand
from python_cqrs_core.base_query import BaseQuery, PaginatedQuery

__version__ = "0.1.0"

__all__ = [
    "ICommand",
    "ICommandHandler",
    "IQuery",
    "IQueryHandler",
    "BaseCommand",
    "BaseQuery",
    "PaginatedQuery",
]
