# Infrastructure: Building APIs

Production-ready FastAPI setup with middleware, error handling, lifespan management, and health checks.

## Example 8: Complete FastAPI Setup with Middleware

Full FastAPI application setup with CORS, error handlers, lifespan hooks, structured logging, and health checks.

```python
from fastapi import FastAPI
from fastapi_middleware_toolkit import (
    setup_cors_middleware,
    setup_error_handlers,
    create_lifespan_manager,
    create_health_check_endpoint,
)
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings
from python_structlog_config import configure_for_production
from python_app_exceptions import BaseApplicationException

# Configure structured logging
configure_for_production(service_name="my-api", version="1.0.0")


# Settings
class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "My API"
    secret_key: str


settings = Settings()


# Lifespan management
async def on_startup():
    print(f"{settings.app_name} starting...")


async def on_shutdown():
    print(f"{settings.app_name} shutting down...")


lifespan = create_lifespan_manager(
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    service_name=settings.app_name,
    service_version="1.0.0",
)

# Create app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

# Setup middleware
setup_cors_middleware(
    app,
    allowed_origins=settings.allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    max_age=settings.cors_max_age,
)

# Setup error handlers
setup_error_handlers(app, BaseApplicationException)

# Health check
health_check = create_health_check_endpoint(
    service_name=settings.app_name,
    version="1.0.0",
    additional_checks={"database": "connected"},
)
app.get("/health")(health_check)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}!"}
```
