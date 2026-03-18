"""Repository use cases (queries and commands)."""

# Query use cases
from .get_by_id import GetByIdHandler, GetByIdQuery
from .get_all import GetAllHandler, GetAllQuery
from .exists import ExistsHandler, ExistsQuery
from .count import CountHandler, CountQuery
from .find_paginated import FindPaginatedHandler, FindPaginatedQuery

# Command use cases
from .create import CreateHandler, CreateCommand
from .update import UpdateHandler, UpdateCommand
from .delete import DeleteHandler, DeleteCommand

__all__ = [
    # Queries
    "GetByIdHandler", "GetByIdQuery",
    "GetAllHandler", "GetAllQuery",
    "ExistsHandler", "ExistsQuery",
    "CountHandler", "CountQuery",
    "FindPaginatedHandler", "FindPaginatedQuery",
    # Commands
    "CreateHandler", "CreateCommand",
    "UpdateHandler", "UpdateCommand",
    "DeleteHandler", "DeleteCommand",
]

