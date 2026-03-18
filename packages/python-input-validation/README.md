# python-input-validation

Business-level input validation and sanitization for Python applications.

## Installation

```bash
pip install python-input-validation
```

## Usage

```python
from python_input_validation import (
    validate_email_format,
    validate_string_length,
    sanitize_email,
    sanitize_text_input
)

# Validate email
is_valid = validate_email_format("user@example.com")  # True

# Validate length
is_valid = validate_string_length("hello", min_length=3, max_length=10)  # True

# Sanitize email
clean_email = sanitize_email("  USER@EXAMPLE.COM  ")  # "user@example.com"

# Sanitize text
clean_text = sanitize_text_input("  hello world  ", max_length=10)  # "hello worl"
```

## Features

- ✅ Email validation
- ✅ Length validation
- ✅ Email sanitization
- ✅ Text sanitization
- ✅ Zero dependencies
- ✅ Framework-agnostic

## License

MIT






