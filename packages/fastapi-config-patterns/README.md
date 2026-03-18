# FastAPI Config Patterns

Reusable Pydantic settings classes for FastAPI applications with common configuration patterns.

**Extracted from:** GridFlow `backend/src/config.py`

## Installation

```bash
pip install fastapi-config-patterns
```

## Features

- **BaseFastAPISettings**: Common FastAPI app settings (debug, host, port, CORS)
- **BaseDatabaseSettings**: Database connection configuration mixin
- **Validators**: Reusable field validators (CORS origins parser)

## Usage

### Basic Settings

```python
from fastapi_config_patterns import BaseFastAPISettings

class Settings(BaseFastAPISettings):
    # Add your app-specific settings
    app_name: str = "my-app"
    secret_key: str

settings = Settings()
print(settings.debug)  # False
print(settings.port)   # 8000
```

### With Database

```python
from fastapi_config_patterns import (
    BaseFastAPISettings,
    BaseDatabaseSettings
)

class Settings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "my-app"

settings = Settings()
print(settings.database_url)  # postgresql+asyncpg://...
```

### CORS Origins Validator

```python
from pydantic import field_validator
from pydantic_settings import BaseSettings
from fastapi_config_patterns import assemble_cors_origins

class Settings(BaseSettings):
    allowed_origins: list[str]
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v):
        return assemble_cors_origins(v)

# From environment variable: ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080"
settings = Settings()
print(settings.allowed_origins)  # ["http://localhost:3000", "http://localhost:8080"]
```

### Environment Variables

The base classes support these environment variables:

```bash
# BaseFastAPISettings
DEBUG=true
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080"

# BaseDatabaseSettings
DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/db"
```

## API Reference

### `BaseFastAPISettings`

Base settings class with common FastAPI configuration.

**Fields:**
- `debug` (bool): Debug mode (default: False, env: DEBUG)
- `api_v1_str` (str): API v1 prefix (default: "/v1")
- `host` (str): Server host (default: "0.0.0.0")
- `port` (int): Server port (default: 8000)
- `allowed_origins` (Union[str, List[str]]): CORS origins
- `cors_allow_credentials` (bool): Allow credentials (default: False)
- `cors_max_age` (int): Preflight cache seconds (default: 600)

### `BaseDatabaseSettings`

Database connection configuration mixin.

**Fields:**
- `database_url` (str): Database connection URL (env: DATABASE_URL)

**Supported databases:**
- PostgreSQL: `postgresql+asyncpg://user:pass@host:port/db`
- SQLite: `sqlite+aiosqlite:///./app.db`

### `assemble_cors_origins(v)`

Parse CORS origins from string or list.

**Args:**
- `v` (Union[str, List[str]]): Origins as string or list

**Returns:**
- `List[str]`: Parsed list of origins

**Handles:**
- Wildcard "*" for all origins
- Comma-separated string
- List of strings

## Dependencies

- `pydantic>=2.0.0`
- `pydantic-settings>=2.0.0`

## License

MIT
