"""Handler registry helpers for bulk and auto registration."""

from typing import List, Tuple, Type, Any
from python_cqrs_core import ICommand, IQuery, ICommandHandler, IQueryHandler
from python_cqrs_dispatcher.dispatcher import CQRSDispatcher


def register_handlers(
    dispatcher: CQRSDispatcher,
    handlers: List[Tuple[Type, Any]]
) -> None:
    """Bulk register command and query handlers.
    
    Args:
        dispatcher: CQRSDispatcher instance
        handlers: List of (request_type, handler) tuples
    
    Raises:
        ValueError: If request type is neither command nor query
    
    Example:
        >>> handlers = [
        ...     (CreateUserCommand, CreateUserHandler()),
        ...     (GetUserQuery, GetUserHandler()),
        ... ]
        >>> register_handlers(dispatcher, handlers)
    """
    for request_type, handler in handlers:
        # Check if command or query based on inheritance
        if issubclass(request_type, ICommand):
            dispatcher.register_command_handler(request_type, handler)
        elif issubclass(request_type, IQuery):
            dispatcher.register_query_handler(request_type, handler)
        else:
            raise ValueError(
                f"Unknown request type: {request_type.__name__}. "
                "Must be ICommand or IQuery"
            )


def auto_register_handlers(
    dispatcher: CQRSDispatcher,
    module
) -> None:
    """Auto-discover and register handlers from module.
    
    Scans module for handler classes and registers them automatically.
    Handlers must implement ICommandHandler or IQueryHandler.
    
    Args:
        dispatcher: CQRSDispatcher instance
        module: Python module to scan
    
    Example:
        >>> import my_app.handlers as handlers_module
        >>> auto_register_handlers(dispatcher, handlers_module)
    """
    import inspect
    
    for name, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
            continue
        
        # Check if it's a handler
        if not hasattr(obj, 'handle'):
            continue
        
        # Try to infer request type from generic base
        if hasattr(obj, '__orig_bases__'):
            for base in obj.__orig_bases__:
                if not hasattr(base, '__origin__'):
                    continue
                
                # Extract generic type parameter
                if hasattr(base, '__args__') and base.__args__:
                    request_type = base.__args__[0]
                    
                    # Instantiate handler
                    handler_instance = obj()
                    
                    # Register based on request type
                    if issubclass(request_type, ICommand):
                        dispatcher.register_command_handler(
                            request_type,
                            handler_instance
                        )
                    elif issubclass(request_type, IQuery):
                        dispatcher.register_query_handler(
                            request_type,
                            handler_instance
                        )
