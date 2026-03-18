"""CloudEvents 1.0 formatter for protocol-level standardization.

Per PRD specifications
"""

from typing import Dict, Any, Optional
from python_outbox_core.events import IOutboxEvent
from python_outbox_core.formatters.base import IEventFormatter


class CloudEventsFormatter(IEventFormatter):
    """Base CloudEvents 1.0 formatter.
    
    Implements CloudEvents specification for protocol-level standardization.
    Can be extended for specific gateways (Kong, etc.).
    
    Spec: https://github.com/cloudevents/spec/blob/v1.0/spec.md
    
    Example:
        >>> formatter = CloudEventsFormatter(
        ...     source="my-service",
        ...     data_content_type="application/json"
        ... )
        >>> formatted = formatter.format(event)
    """
    
    def __init__(
        self,
        source: str,
        data_content_type: str = "application/json"
    ):
        """Initialize CloudEvents formatter.
        
        Args:
            source: Event source identifier (e.g., "my-service")
            data_content_type: Content type of event data
        """
        self.source = source
        self.data_content_type = data_content_type
    
    def format(self, event: IOutboxEvent) -> Dict[str, Any]:
        """Format event as CloudEvents 1.0.
        
        Args:
            event: Outbox event to format
        
        Returns:
            CloudEvents 1.0 formatted dictionary
        """
        cloud_event = {
            # Required CloudEvents fields
            "specversion": "1.0",
            "type": event.event_type,
            "source": self.source,
            "id": str(event.event_id),
            "time": event.occurred_at.isoformat(),
            "datacontenttype": self.data_content_type,
            "data": event.to_message(),
            
            # Optional CloudEvents extension fields
            "subject": event.aggregate_id,
        }
        
        # Add correlation ID if present
        if hasattr(event, 'correlation_id') and event.correlation_id:
            cloud_event["correlationid"] = str(event.correlation_id)
        
        # Allow subclasses to enrich metadata
        return self.enrich_metadata(cloud_event)
    
    def enrich_metadata(
        self,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Hook for subclasses to enrich metadata.
        
        Override this in subclasses (e.g., Kong formatter) to add
        gateway-specific metadata.
        
        Args:
            event_data: CloudEvents formatted data
        
        Returns:
            Enriched event data
        
        Example:
            >>> class KongFormatter(CloudEventsFormatter):
            ...     def enrich_metadata(self, event_data):
            ...         event_data["kong_namespace"] = "production"
            ...         return event_data
        """
        return event_data
    
    def get_content_type(self) -> str:
        """CloudEvents content type.
        
        Returns:
            CloudEvents JSON content type
        """
        return "application/cloudevents+json"
