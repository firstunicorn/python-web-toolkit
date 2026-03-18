# Python Structlog Config

Structured logging configuration with optional OpenTelemetry and Sentry integration.

**Extracted from:** GridFlow `backend/src/infrastructure/logging_config.py`

## Installation

```bash
# Basic installation
pip install python-structlog-config

# With OTel support
pip install python-structlog-config[otel]

# With Sentry support
pip install python-structlog-config[sentry]

# With all integrations
pip install python-structlog-config[all]
```

## Features

- **Structured Logging**: JSON or console output
- **OpenTelemetry**: Optional OTel instrumentation
- **Sentry**: Optional Sentry error tracking
- **Presets**: Development, production, and testing configurations

## Usage

### Quick Start

```python
from python_structlog_config import configure_for_development, get_logger

# Configure logging for development
configure_for_development("my-api")

# Get logger
logger = get_logger(__name__)
logger.info("Application started", version="1.0.0")
```

### Production Setup

```python
from python_structlog_config import configure_for_production

configure_for_production(
    "my-api",
    sentry_dsn="https://...@sentry.io/...",
    log_level="INFO"
)
```

### Custom Configuration

```python
from python_structlog_config import configure_structlog

configure_structlog(
    log_level="DEBUG",
    json_output=True,
    enable_otel=True,
    enable_sentry=True,
    sentry_dsn="https://...@sentry.io/...",
    service_name="my-api",
    environment="staging"
)
```

### Testing Setup

```python
from python_structlog_config import configure_for_testing

configure_for_testing("my-api")
```

## Presets

### Development

- **Log Level**: DEBUG
- **Output**: Console (human-readable)
- **OTel**: Disabled
- **Sentry**: Disabled

### Production

- **Log Level**: INFO
- **Output**: JSON
- **OTel**: Enabled
- **Sentry**: Optional (if DSN provided)

### Testing

- **Log Level**: WARNING
- **Output**: Console
- **OTel**: Disabled
- **Sentry**: Disabled

## API Reference

### `configure_structlog(...)`

Configure structlog with optional integrations.

**Parameters:**
- `log_level` (str): Logging level (default: "INFO")
- `json_output` (bool): Use JSON renderer (default: False)
- `enable_otel` (bool): Enable OTel (default: False)
- `enable_sentry` (bool): Enable Sentry (default: False)
- `sentry_dsn` (Optional[str]): Sentry DSN
- `service_name` (Optional[str]): Service name
- `environment` (Optional[str]): Environment name

### `get_logger(name=None)`

Get a structlog logger instance.

**Parameters:**
- `name` (Optional[str]): Logger name

**Returns:**
- Structlog logger instance

### Presets

- `configure_for_development(service_name)`: Development preset
- `configure_for_production(service_name, sentry_dsn, log_level)`: Production preset
- `configure_for_testing(service_name)`: Testing preset

## Integrations

### OpenTelemetry

Requires: `pip install python-structlog-config[otel]`

```python
configure_structlog(enable_otel=True, service_name="my-api")
```

### Sentry

Requires: `pip install python-structlog-config[sentry]`

```python
configure_structlog(
    enable_sentry=True,
    sentry_dsn="https://...@sentry.io/...",
    environment="production"
)
```

## Dependencies

- `structlog>=23.0.0`

**Optional:**
- `opentelemetry-instrumentation-logging>=0.40b0` (OTel)
- `sentry-sdk>=1.40.0` (Sentry)

## License

MIT
