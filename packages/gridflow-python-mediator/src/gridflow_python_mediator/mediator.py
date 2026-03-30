"""Core mediator for request/response dispatch.

Extracted from GridFlow backend/src/apps/token_generator/application/common/mediator/mediator.py
"""

from typing import TypeVar, Type, Dict, Any, Callable, List
import inspect

TRequest = TypeVar('TRequest')
TResult = TypeVar('TResult')


class Mediator:
    """Generic request/response dispatcher (Mediator pattern).
    
    Decouples senders from handlers, allowing for:
    - Pipeline behaviors (logging, timing, validation)
    - Dynamic handler registration
    - Type-safe dispatch
    
    Example:
        >>> mediator = Mediator()
        >>> mediator.register_handler(MyRequest, MyHandler())
        >>> result = await mediator.send(MyRequest(...))
    """
    
    def __init__(self):
        """Initialize mediator with empty handler registry."""
        self._handlers: Dict[Type, Any] = {}
        self._behaviors: List[Callable] = []
    
    def register_handler(
        self,
        request_type: Type[TRequest],
        handler: Any
    ) -> None:
        """Register handler for request type.
        
        Args:
            request_type: Request/Command/Query type
            handler: Handler instance with handle() method
        
        Raises:
            ValueError: If handler already registered for type
        
        Example:
            >>> mediator.register_handler(CreateUserCommand, CreateUserHandler())
        """
        if request_type in self._handlers:
            raise ValueError(
                f"Handler already registered for {request_type.__name__}"
            )
        self._handlers[request_type] = handler
    
    async def send(self, request: TRequest) -> TResult:
        """Dispatch request to its registered handler.
        
        Executes pipeline behaviors before calling handler.
        
        Args:
            request: Request/Command/Query to send
        
        Returns:
            Result from handler
        
        Raises:
            ValueError: If no handler registered for request type
        
        Example:
            >>> cmd = CreateUserCommand(name="John")
            >>> user_id = await mediator.send(cmd)
        """
        request_type = type(request)
        handler = self._handlers.get(request_type)
        
        if not handler:
            raise ValueError(
                f"No handler registered for {request_type.__name__}"
            )
        
        # Execute pipeline behaviors
        for behavior in self._behaviors:
            # Behaviors can modify request or short-circuit
            result = await behavior(request, handler)
            if result is not None:
                return result
        
        # Execute handler
        if inspect.iscoroutinefunction(handler.handle):
            return await handler.handle(request)
        else:
            return handler.handle(request)
    
    def add_pipeline_behavior(self, behavior: Callable) -> None:
        """Add pipeline behavior for cross-cutting concerns.
        
        Behaviors are executed in order before handler.
        Can implement logging, timing, validation, etc.
        
        Args:
            behavior: Async function(request, handler) -> Optional[result]
        
        Example:
            >>> async def logging_behavior(request, handler):
            ...     print(f"Handling {type(request).__name__}")
            ...     return None  # Continue to handler
            >>> 
            >>> mediator.add_pipeline_behavior(logging_behavior)
        """
        self._behaviors.append(behavior)
