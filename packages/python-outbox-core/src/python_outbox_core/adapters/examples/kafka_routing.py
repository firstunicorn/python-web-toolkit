"""Kafka partition key routing example.

EDUCATIONAL EXAMPLE - NOT production-ready.
Demonstrates "Few Topics + Partition Keys" best practice.

Best Practices (from PRD):
- Use 3-10 topics (not hundreds per user/interest)
- Route via partition keys (get_partition_key() method)
- Filter in consumers (interests, content_type in metadata)
- AVOID anti-pattern: separate topics per entity
"""

from typing import Dict, Any, Optional
from python_outbox_core.events import IOutboxEvent
from python_outbox_core.formatters import CloudEventsFormatter


class PartitionKeyRouter:
    """Example: Route events to Kafka partitions by key.

    Uses event.get_partition_key() for consistent partition routing.
    Same aggregate_id always goes to same partition (ordering).

    Example:
        >>> router = PartitionKeyRouter(topic_prefix="gridflow")
        >>> topic, key = router.route(event)
        >>> # topic = "gridflow.domain-events"
        >>> # key = "invite-123"  (from aggregate_id)
    """

    def __init__(
        self,
        topic_prefix: str,
        default_topic: str = "domain-events"
    ):
        self.topic_prefix = topic_prefix
        self.default_topic = default_topic

    def route(self, event: IOutboxEvent) -> tuple:
        """Determine topic and partition key for event.

        Args:
            event: Outbox event to route

        Returns:
            Tuple of (topic_name, partition_key)
        """
        topic = f"{self.topic_prefix}.{self.default_topic}"
        partition_key = event.get_partition_key()
        return topic, partition_key


class KafkaRoutingFormatter(CloudEventsFormatter):
    """Example: CloudEvents formatter with Kafka routing metadata.

    Adds partition key and topic hint to CloudEvent metadata.

    Example:
        >>> formatter = KafkaRoutingFormatter(
        ...     source="gridflow-api",
        ...     topic_prefix="gridflow"
        ... )
        >>> formatted = formatter.format(event)
    """

    def __init__(
        self,
        source: str,
        topic_prefix: str = "app",
        default_topic: str = "domain-events"
    ):
        super().__init__(source=source)
        self._router = PartitionKeyRouter(topic_prefix, default_topic)

    def enrich_metadata(
        self,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add Kafka routing metadata to CloudEvent."""
        event = event_data.get("_source_event")
        if event and hasattr(event, "get_partition_key"):
            topic, key = self._router.route(event)
            event_data["kafkatopic"] = topic
            event_data["kafkapartitionkey"] = key
        return event_data
