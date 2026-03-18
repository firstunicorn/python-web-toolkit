"""Query interfaces for CQRS pattern.

Extracted from GridFlow backend/src/apps/token_generator/application/common/ports_interfaces/query.py
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TQuery = TypeVar('TQuery', bound='IQuery')
TResult = TypeVar('TResult')


class IQuery(ABC):
    """Base query interface (read operations).
    
    Queries read state without modifying it.
    Use this as a marker interface for all queries.
    
    Example:
        >>> from pydantic import BaseModel
        >>> 
        >>> class GetUserQuery(BaseModel, IQuery):
        ...     user_id: int
    """
    pass


class IQueryHandler(ABC, Generic[TQuery, TResult]):
    """Query handler interface.
    
    Handles a specific query type and returns a result.
    
    Example:
        >>> class GetUserHandler(IQueryHandler[GetUserQuery, User]):
        ...     async def handle(self, query: GetUserQuery) -> User:
        ...         # Fetch user logic
        ...         return user
    """
    
    @abstractmethod
    async def handle(self, query: TQuery) -> TResult:
        """Handle the query.
        
        Args:
            query: Query to handle
        
        Returns:
            Query result
        """
        pass
