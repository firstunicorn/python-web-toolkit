# Infrastructure: Messaging Patterns

Transactional outbox pattern for reliable event publishing with CloudEvents formatting.

## Example 14: Transactional Outbox Pattern

Reliable event publishing using the transactional outbox pattern with CloudEvents and Kafka routing.

```python
from datetime import datetime
from python_outbox_core import (
    IOutboxEvent,
    CloudEventsFormatter,
    IOutboxRepository,
)
from python_outbox_core.adapters.examples import KafkaRoutingFormatter


# Define outbox event
class OrderCreatedEvent(IOutboxEvent):
    aggregate_id: str
    aggregate_type: str = "Order"
    event_type: str = "order.created"
    payload: dict
    occurred_at: datetime

    def to_message(self) -> dict:
        return {
            "order_id": self.aggregate_id,
            "customer_id": self.payload["customer_id"],
            "total": self.payload["total"],
        }


# Create event
event = OrderCreatedEvent(
    aggregate_id="order-123",
    payload={"customer_id": "cust-456", "total": 99.99},
    occurred_at=datetime.utcnow(),
)

# Save to outbox table (within transaction)
async with db.begin():
    # 1. Save order to database
    order = Order(id="order-123", total=99.99)
    db.add(order)

    # 2. Save event to outbox (same transaction)
    outbox_repo: IOutboxRepository = OutboxRepository(db)
    await outbox_repo.save(event)

# Background worker publishes events
formatter = CloudEventsFormatter(source="my-api", data_content_type="application/json")
message = formatter.format(event)

# Kafka routing example
kafka_formatter = KafkaRoutingFormatter(source="my-api", topic_prefix="orders")
message = kafka_formatter.format(event)
partition_key = event.get_partition_key()  # Returns aggregate_id by default
```
