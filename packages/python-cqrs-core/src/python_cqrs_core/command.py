"""Command interfaces for CQRS pattern.

Extracted from GridFlow backend/src/apps/token_generator/application/common/ports_interfaces/command.py
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TCommand = TypeVar('TCommand', bound='ICommand')
TResult = TypeVar('TResult')


class ICommand(ABC):
    """Base command interface (write operations).
    
    Commands modify state and may return a result.
    Use this as a marker interface for all commands.
    
    Example:
        >>> from pydantic import BaseModel
        >>> 
        >>> class CreateUserCommand(BaseModel, ICommand):
        ...     name: str
        ...     email: str
    """
    pass


class ICommandHandler(ABC, Generic[TCommand, TResult]):
    """Command handler interface.
    
    Handles a specific command type and returns a result.
    
    Example:
        >>> class CreateUserHandler(ICommandHandler[CreateUserCommand, User]):
        ...     async def handle(self, command: CreateUserCommand) -> User:
        ...         # Create user logic
        ...         return user
    """
    
    @abstractmethod
    async def handle(self, command: TCommand) -> TResult:
        """Handle the command.
        
        Args:
            command: Command to handle
        
        Returns:
            Command result
        """
        pass
