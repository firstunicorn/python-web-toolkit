# fastapi-config-patterns

Reusable Pydantic settings classes for FastAPI applications.

## Installation

```bash
pip install fastapi-config-patterns
```

## Public API

| Class/Function | Purpose |
|----------------|---------|
| `BaseFastAPISettings` | Base settings with `app_name`, `debug`, `allowed_origins`, env loading |
| `BaseDatabaseSettings` | Database settings mixin (`database_url`, pool config) |
| `assemble_cors_origins(v)` | Parse CORS origins from string or list |

## Usage

```python
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings

class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    redis_url: str = "redis://localhost"

settings = Settings()  # loads from environment / .env
```
