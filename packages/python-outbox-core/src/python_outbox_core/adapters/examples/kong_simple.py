"""Minimal Kong AI Gateway adapter example.

EDUCATIONAL EXAMPLE - NOT production-ready.
For production use: python-kong-integration package.

Shows how to extend CloudEventsFormatter for Kong AI Gateway.
"""

from typing import Dict, Any
from python_outbox_core.formatters import CloudEventsFormatter


class KongSimpleFormatter(CloudEventsFormatter):
    """Example: Kong AI Gateway CloudEvents formatter.

    Extends CloudEventsFormatter with Kong-specific metadata
    (namespace, consumer group, rate limit tier).

    Example:
        >>> formatter = KongSimpleFormatter(
        ...     source="my-service",
        ...     kong_namespace="production"
        ... )
        >>> formatted = formatter.format(event)
    """

    def __init__(
        self,
        source: str,
        kong_namespace: str = "default",
        consumer_group: str = "default",
        rate_limit_tier: str = "standard"
    ):
        super().__init__(source=source)
        self.kong_namespace = kong_namespace
        self.consumer_group = consumer_group
        self.rate_limit_tier = rate_limit_tier

    def enrich_metadata(
        self,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add Kong-specific metadata to CloudEvent."""
        event_data["kongnamespace"] = self.kong_namespace
        event_data["kongconsumergroup"] = self.consumer_group
        event_data["kongratelimittier"] = self.rate_limit_tier
        return event_data
