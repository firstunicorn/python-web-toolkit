# python-infrastructure-exceptions

Typed exceptions for infrastructure layer failures (database, cache, messaging, external services).

## Installation

```bash
pip install python-infrastructure-exceptions
```

## Public API

| Exception | Extra fields |
|-----------|-------------|
| `InfrastructureException` | `message`, `details` |
| `DatabaseError` | `query` |
| `CacheError` | `cache_backend`, `key` |
| `ConfigurationError` | `config_key` |
| `ExternalServiceError` | `service_name`, `status_code` |
| `MessageQueueError` | `broker`, `topic` |

## Usage

```python
from python_infrastructure_exceptions import DatabaseError, CacheError

raise DatabaseError("Connection lost", query="SELECT ...", details={...})
raise CacheError("Timeout", cache_backend="redis", key="user:123")
```

See also: [exception libraries comparison](../exception-comparison)
