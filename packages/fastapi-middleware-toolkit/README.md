# FastAPI Middleware Toolkit

Reusable FastAPI middleware setup functions for CORS, error handlers, and lifespan management.

**Extracted from:** GridFlow `backend/src/infrastructure` and `backend/src/middleware`

## Installation

```bash
pip install fastapi-middleware-toolkit
```

## Features

- **CORS Middleware**: Secure CORS configuration with sensible defaults
- **Error Handlers**: Global error handling for HTTP, validation, and custom exceptions
- **Lifespan Management**: Generic lifespan context manager for startup/shutdown tasks
- **Health Check**: Health check endpoint factory
- **Cache-Control Middleware**: Automatic Cache-Control headers with safe defaults

## Usage

### CORS Middleware

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import setup_cors_middleware

app = FastAPI()

setup_cors_middleware(
    app,
    allowed_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=False,
    allowed_methods=["GET", "POST"],
    max_age=600
)
```

### Error Handlers

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import setup_error_handlers
from python_app_exceptions import BaseApplicationException

app = FastAPI()

# Setup with custom exception class
setup_error_handlers(app, BaseApplicationException)
```

### Lifespan Management

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import create_lifespan_manager

async def init_database():
    print("Database initialized")

async def cleanup_database():
    print("Database cleaned up")

lifespan = create_lifespan_manager(
    on_startup=init_database,
    on_shutdown=cleanup_database,
    service_name="my-api",
    service_version="1.0.0"
)

app = FastAPI(lifespan=lifespan)
```

### Health Check Endpoint

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import create_health_check_endpoint

app = FastAPI()

health_check = create_health_check_endpoint(
    service_name="my-api",
    version="1.0.0",
    additional_checks={"database": "connected"}
)

app.get("/health")(health_check)
```

### Cache-Control Middleware

```python
from fastapi import FastAPI, Response
from fastapi_middleware_toolkit import setup_cache_control_middleware

app = FastAPI()

# Setup with default policy (moderate caching)
setup_cache_control_middleware(app)

# Or customize the default
setup_cache_control_middleware(
    app,
    default_cache_control="public, max-age=3600"
)

# Routes can override the default
@app.get("/sensitive")
def sensitive_endpoint(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return {"data": "sensitive"}

# Routes without explicit Cache-Control get the default
@app.get("/public")
def public_endpoint():
    return {"data": "public"}  # Gets default Cache-Control
```

## API Reference

### `setup_cors_middleware(app, allowed_origins, ...)`

Setup CORS middleware with secure defaults.

**Parameters:**
- `app` (FastAPI): FastAPI application instance
- `allowed_origins` (Union[str, List[str]]): Allowed origins
- `allow_credentials` (bool): Allow credentials (default: False)
- `allowed_methods` (List[str]): HTTP methods (default: ["GET", "POST"])
- `allowed_headers` (List[str]): Allowed headers (default: standard headers)
- `max_age` (int): Preflight cache time in seconds (default: 600)

### `setup_error_handlers(app, custom_exception_class=None)`

Setup global error handlers.

**Parameters:**
- `app` (FastAPI): FastAPI application instance
- `custom_exception_class` (Optional[Type[Exception]]): Custom exception class

### `create_lifespan_manager(on_startup, on_shutdown, ...)`

Create lifespan context manager.

**Parameters:**
- `on_startup` (Optional[Callable]): Startup function
- `on_shutdown` (Optional[Callable]): Shutdown function
- `service_name` (str): Service name (default: "api")
- `service_version` (str): Service version (default: "1.0.0")

### `create_health_check_endpoint(service_name, version, ...)`

Create health check endpoint function.

**Parameters:**
- `service_name` (str): Service name
- `version` (str): Service version (default: "1.0.0")
- `additional_checks` (Optional[Dict]): Additional health data

### `setup_cache_control_middleware(app, default_cache_control)`

Setup Cache-Control middleware with safe defaults.

**Parameters:**
- `app` (FastAPI): FastAPI application instance
- `default_cache_control` (str): Default Cache-Control header value (default: "public, max-age=60, stale-while-revalidate=30")

**Common patterns:**
- `"public, max-age=60, stale-while-revalidate=30"` - Moderate caching (default)
- `"no-store"` - No caching for sensitive data
- `"public, max-age=3600"` - 1 hour cache
- `"private, max-age=0, must-revalidate"` - Browser only, always validate

## Dependencies

- `fastapi>=0.100.0`
- `structlog>=23.0.0`

## License

MIT
