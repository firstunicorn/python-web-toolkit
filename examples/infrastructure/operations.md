# Infrastructure: Operations

Operational concerns including structured logging, monitoring, and observability.

## Example 9: Structured Logging Configuration

Environment-specific logging presets for development, production, and testing.

```python
from python_structlog_config import (
    configure_for_development,
    configure_for_production,
    configure_for_testing,
    get_logger,
)

# Development: console output with colors
configure_for_development()
logger = get_logger(__name__)
logger.info("Starting development server", port=8000)

# Production: JSON output for log aggregation
configure_for_production(
    service_name="my-api",
    version="1.0.0",
    enable_opentelemetry=True,
    enable_sentry=True,
)
logger = get_logger(__name__)
logger.info("Processing request", user_id=123, action="create_order")

# Testing: minimal output
configure_for_testing()
logger = get_logger(__name__)
logger.debug("Test assertion", expected=True, actual=True)

# Structured context
logger.bind(request_id="req-123", user_id=456).info(
    "Order created",
    order_id=789,
    total_amount=99.99,
)
```
