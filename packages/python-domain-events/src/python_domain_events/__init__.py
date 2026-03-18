"""Python Domain Events - Base classes for internal domain events."""

from python_domain_events.base import BaseDomainEvent
from python_domain_events.handler import IDomainEventHandler
from python_domain_events.dispatcher import InProcessEventDispatcher

__version__ = "0.1.0"

__all__ = [
    "BaseDomainEvent",
    "IDomainEventHandler",
    "InProcessEventDispatcher",
]
