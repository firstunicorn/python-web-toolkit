"""Domain event handler interface."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from python_domain_events.base import BaseDomainEvent


TEvent = TypeVar("TEvent", bound=BaseDomainEvent)


class IDomainEventHandler(ABC, Generic[TEvent]):
    """
    Interface for domain event handlers.
    
    Handlers process domain events in-process.
    Each handler should be idempotent and handle one event type.
    """
    
    @abstractmethod
    async def handle(self, event: TEvent) -> None:
        """
        Handle a domain event.
        
        Args:
            event: The domain event to process
        """
        pass
