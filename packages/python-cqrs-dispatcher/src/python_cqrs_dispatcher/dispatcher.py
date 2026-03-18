"""CQRS dispatcher integrating CQRS core with mediator pattern."""

from python_cqrs_core import ICommand, IQuery, ICommandHandler, IQueryHandler
from python_mediator import Mediator
from typing import Type, Any, Dict


class CQRSDispatcher:
    """Dispatcher specialized for CQRS pattern.
    
    Integrates python-cqrs-core with python-mediator, providing:
    - Type-safe command/query dispatch
    - Separate command/query handler registration
    - Pipeline behavior support through mediator
    
    Example:
        >>> dispatcher = CQRSDispatcher()
        >>> dispatcher.register_command_handler(
        ...     CreateUserCommand,
        ...     CreateUserHandler()
        ... )
        >>> user_id = await dispatcher.send_command(cmd)
    """
    
    def __init__(self):
        """Initialize dispatcher with internal mediator."""
        self._mediator = Mediator()
        self._command_handlers: Dict[Type[ICommand], ICommandHandler] = {}
        self._query_handlers: Dict[Type[IQuery], IQueryHandler] = {}
    
    def register_command_handler(
        self,
        command_type: Type[ICommand],
        handler: ICommandHandler
    ) -> None:
        """Register type-safe command handler.
        
        Args:
            command_type: Command class
            handler: Command handler instance
        
        Raises:
            ValueError: If handler already registered
        
        Example:
            >>> dispatcher.register_command_handler(
            ...     CreateUserCommand,
            ...     CreateUserHandler()
            ... )
        """
        if command_type in self._command_handlers:
            raise ValueError(
                f"Handler already registered for {command_type.__name__}"
            )
        
        self._command_handlers[command_type] = handler
        self._mediator.register_handler(command_type, handler)
    
    def register_query_handler(
        self,
        query_type: Type[IQuery],
        handler: IQueryHandler
    ) -> None:
        """Register type-safe query handler.
        
        Args:
            query_type: Query class
            handler: Query handler instance
        
        Raises:
            ValueError: If handler already registered
        
        Example:
            >>> dispatcher.register_query_handler(
            ...     GetUserQuery,
            ...     GetUserHandler()
            ... )
        """
        if query_type in self._query_handlers:
            raise ValueError(
                f"Handler already registered for {query_type.__name__}"
            )
        
        self._query_handlers[query_type] = handler
        self._mediator.register_handler(query_type, handler)
    
    async def send_command(self, command: ICommand) -> Any:
        """Dispatch command with validation.
        
        Args:
            command: Command to dispatch
        
        Returns:
            Command result
        
        Raises:
            ValueError: If no handler registered
        
        Example:
            >>> cmd = CreateUserCommand(name="John")
            >>> user_id = await dispatcher.send_command(cmd)
        """
        command_type = type(command)
        if command_type not in self._command_handlers:
            raise ValueError(
                f"No handler for command {command_type.__name__}"
            )
        return await self._mediator.send(command)
    
    async def send_query(self, query: IQuery) -> Any:
        """Dispatch query with validation.
        
        Args:
            query: Query to dispatch
        
        Returns:
            Query result
        
        Raises:
            ValueError: If no handler registered
        
        Example:
            >>> query = GetUserQuery(user_id=1)
            >>> user = await dispatcher.send_query(query)
        """
        query_type = type(query)
        if query_type not in self._query_handlers:
            raise ValueError(
                f"No handler for query {query_type.__name__}"
            )
        return await self._mediator.send(query)
    
    def add_pipeline_behavior(self, behavior) -> None:
        """Add pipeline behavior to mediator.
        
        Behaviors execute before all command/query handlers.
        
        Args:
            behavior: Pipeline behavior function
        
        Example:
            >>> from python_mediator import LoggingBehavior
            >>> dispatcher.add_pipeline_behavior(
            ...     LoggingBehavior().handle
            ... )
        """
        self._mediator.add_pipeline_behavior(behavior)
