# python-input-validation

Business-level input validation and sanitization.

## Installation

```bash
pip install python-input-validation
```

## Public API

### validators

| Function | Purpose |
|----------|---------|
| `validate_email_format(email) -> bool` | Validate email format |
| `validate_string_length(text, min_length, max_length) -> bool` | Check string length constraints |

### sanitizers

| Function | Purpose |
|----------|---------|
| `sanitize_email(email) -> str` | Normalize email input |
| `sanitize_text_input(text, max_length) -> str` | Strip/truncate text |

## Usage

```python
from python_input_validation import validate_email_format, sanitize_email

clean = sanitize_email("  User@Example.COM  ")  # "user@example.com"
valid = validate_email_format(clean)  # True
```
