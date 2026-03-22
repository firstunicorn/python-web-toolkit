# postgres-data-sanitizers

PostgreSQL data sanitization: null character escaping, surrogate detection, JSONB-safe dictionaries.

## Installation

```bash
pip install postgres-data-sanitizers
```

## Public API

| Function | Purpose |
|----------|---------|
| `escape_null_chars(text) -> str` | Escape `\x00` to unicode representation |
| `unescape_null_chars(text) -> str` | Reverse escape |
| `sanitize_dict_for_postgres(data) -> dict` | Recursively escape nulls in dict (JSONB) |
| `unescape_dict_from_postgres(data) -> dict` | Reverse dict escape |
| `validate_postgres_text(text) -> str\|None` | Validate and escape text for storage |
| `contains_surrogates(text) -> bool` | Detect UTF-8 surrogate characters |

## Usage

```python
from postgres_data_sanitizers import sanitize_dict_for_postgres

safe = sanitize_dict_for_postgres({"bio": "text\x00with\x00nulls"})
# nulls escaped for PostgreSQL JSONB storage
```
