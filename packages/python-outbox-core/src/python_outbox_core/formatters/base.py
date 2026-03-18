"""Base event formatter protocol for extensibility.

Per PRD specifications - Strategy Pattern for formatter extensibility
"""

from typing import Protocol, Dict, Any
from python_outbox_core.events import IOutboxEvent


class IEventFormatter(Protocol):
    """Protocol for extensible event formatting (Strategy Pattern).
    
    Allows projects to customize event format for different brokers/gateways.
    Examples: CloudEvents, Kong AI Gateway, custom formats.
    
    Example:
        >>> class CustomFormatter(IEventFormatter):
        ...     def format(self, event: IOutboxEvent) -> Dict[str, Any]:
        ...         return {"custom": event.to_message()}
        ...     
        ...     def get_content_type(self) -> str:
        ...         return "application/custom+json"
    """
    
    def format(self, event: IOutboxEvent) -> Dict[str, Any]:
        """Format event for publishing.
        
        Args:
            event: Outbox event to format
            
        Returns:
            Formatted event as dictionary ready for broker
        
        Example:
            >>> formatter = CloudEventsFormatter("my-service")
            >>> formatted = formatter.format(event)
        """
        ...
    
    def get_content_type(self) -> str:
        """Get content type for formatted event.
        
        Returns:
            Content type string (e.g., 'application/cloudevents+json')
        
        Example:
            >>> formatter.get_content_type()
            'application/cloudevents+json'
        """
        ...
