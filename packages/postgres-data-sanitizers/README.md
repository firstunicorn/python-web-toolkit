# postgres-data-sanitizers

PostgreSQL-specific data sanitization (null chars, surrogates).

## Installation

```bash
pip install postgres-data-sanitizers
```

## Usage

```python
from postgres_data_sanitizers import (
    escape_null_chars,
    sanitize_dict_for_postgres,
    validate_postgres_text,
    contains_surrogates
)

# Escape null characters in strings
safe_text = escape_null_chars("hello\x00world")  # "hello\\u0000world"

# Sanitize dictionaries for JSONB storage
data = {"key": "value\x00with\x00nulls"}
safe_data = sanitize_dict_for_postgres(data)

# Validate text fields
text = validate_postgres_text("user input\x00")

# Check for surrogate characters
has_surrogates = contains_surrogates(text)
```

## Features

- ✅ Escapes null characters (preserves data)
- ✅ JSONB-safe dictionary sanitization
- ✅ Surrogate character detection
- ✅ Zero dependencies
- ✅ Prevents database crashes

## Why This Matters

PostgreSQL rejects null characters (`\x00`) in TEXT/VARCHAR/JSONB fields, causing:
```
asyncpg.exceptions.UntranslatableCharacterError
```

This library **escapes** rather than **removes** null characters, preserving data integrity.

## License

MIT






