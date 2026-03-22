# python-structlog-config

Structured logging configuration with optional OpenTelemetry and Sentry integration.

## Installation

```bash
pip install python-structlog-config
```

## Public API

| Function | Purpose |
|----------|---------|
| `configure_structlog(log_level, json_output, ...)` | Core configuration |
| `get_logger(name)` | Get structlog logger |
| `configure_for_development(service_name)` | Dev preset: console, debug |
| `configure_for_production(service_name, sentry_dsn)` | Prod preset: JSON, OTel, Sentry |
| `configure_for_testing(service_name)` | Test preset: minimal, warning |
| `setup_otel_logging(service_name)` | OpenTelemetry integration |
| `setup_sentry_logging(sentry_dsn, environment)` | Sentry integration |

## Usage

```python
from python_structlog_config import configure_for_development, get_logger

configure_for_development("my-service")
logger = get_logger(__name__)
logger.info("started", port=8000)
```

## Production setup

```python
from python_structlog_config import configure_for_production

configure_for_production(
    service_name="api",
    sentry_dsn="https://...",
    log_level="INFO",
)
```
