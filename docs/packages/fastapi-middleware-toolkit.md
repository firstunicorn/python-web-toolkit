# fastapi-middleware-toolkit

Reusable FastAPI middleware: CORS, error handlers, cache control, lifespan, health checks.

## Installation

```bash
pip install fastapi-middleware-toolkit
```

## Public API

| Function/Class | Purpose |
|----------------|---------|
| `setup_cors_middleware(app, allowed_origins, ...)` | CORS with secure defaults |
| `setup_error_handlers(app, custom_exception_class)` | Global error handlers |
| `CacheControlMiddleware` | Default Cache-Control headers |
| `setup_cache_control_middleware(app)` | Register cache control |
| `create_lifespan_manager(on_startup, on_shutdown)` | Lifespan context manager |
| `create_health_check_endpoint(service_name, version)` | Health check factory |

## Usage

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import (
    setup_cors_middleware,
    setup_error_handlers,
    create_lifespan_manager,
)

lifespan = create_lifespan_manager(service_name="api")
app = FastAPI(lifespan=lifespan)
setup_cors_middleware(app, ["http://localhost:3000"])
setup_error_handlers(app)
```
