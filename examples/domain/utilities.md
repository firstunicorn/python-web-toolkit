# Domain Layer: Utilities

Examples of general-purpose utilities for string operations and date/time handling.

## Example 4: String Utilities

Text transformations, filename sanitization, truncation, and whitespace normalization.

```python
from python_technical_primitives.text import (
    to_sentence_case,
    to_lower_case,
    to_upper_case,
    sanitize_filename,
    truncate,
    normalize_whitespace
)

# Case conversions
text = "HELLO WORLD"
sentence = to_sentence_case(text)  # "Hello world"
lower = to_lower_case(text)        # "hello world"
upper = to_upper_case("hello")     # "HELLO"

# Sanitize filenames
user_filename = "my document?.txt"
safe_filename = sanitize_filename(user_filename)  # "my_document.txt"

# Truncate long text
long_text = "This is a very long description that needs to be truncated"
short = truncate(long_text, 30)  # "This is a very long descri..."

# Normalize whitespace
messy = "Too    many     spaces"
clean = normalize_whitespace(messy)  # "Too many spaces"
```

## Example 5: DateTime Operations

Timezone-aware date/time operations, expiry checks, and ISO string formatting.

```python
from python_technical_primitives.datetime import (
    utc_now,
    add_days,
    add_hours,
    is_expired,
    days_until,
    to_iso_string
)

# Current time (timezone-aware)
now = utc_now()

# Calculate expiry (7 days from now)
expiry = add_days(now, 7)

# Check if expired
if is_expired(expiry):
    print("Token expired!")
else:
    remaining = days_until(expiry)
    print(f"{remaining} days remaining")

# ISO string conversion
iso = to_iso_string(now)  # "2025-12-28T17:30:00+00:00"
```
