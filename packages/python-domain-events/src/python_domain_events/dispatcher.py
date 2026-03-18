"""In-process event dispatcher for domain events."""

import logging
from typing import Dict, List, Type, Any
from python_domain_events.base import BaseDomainEvent
from python_domain_events.handler import IDomainEventHandler


logger = logging.getLogger(__name__)


class InProcessEventDispatcher:
    """
    Dispatches domain events to registered handlers in-process.
    
    This dispatcher is for internal domain events within the same service.
    For cross-service events, use the Outbox pattern with Kafka.
    """
    
    def __init__(self):
        self._handlers: Dict[Type[BaseDomainEvent], List[IDomainEventHandler]] = {}
    
    def register(
        self,
        event_type: Type[BaseDomainEvent],
        handler: IDomainEventHandler
    ) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.debug(f"Registered {handler.__class__.__name__} for {event_type.__name__}")
    
    async def dispatch(self, event: BaseDomainEvent) -> None:
        """
        Dispatch event to all registered handlers.
        
        Args:
            event: Domain event to dispatch
        """
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])
        
        if not handlers:
            logger.warning(f"No handlers registered for {event_type.__name__}")
            return
        
        logger.info(f"Dispatching {event.event_type} (ID: {event.event_id})")
        
        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception as e:
                logger.error(
                    f"Handler {handler.__class__.__name__} failed: {e}",
                    exc_info=True
                )
                raise
    
    def clear(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
