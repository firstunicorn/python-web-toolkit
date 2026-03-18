# python-app-exceptions

Base exception hierarchy for Python web applications.

## Installation

```bash
pip install python-app-exceptions
```

## Usage

```python
from python_app_exceptions import (
    BaseApplicationException,
    BusinessLogicError,
    ValidationError,
    InvalidInputError,
    RetryExhaustedException,
    RetryableError
)

# Raise validation errors
raise ValidationError("email", "invalid@", "Invalid email format")

# Raise business logic errors
raise BusinessLogicError("user_must_be_active", "User account is disabled")

# Raise retry errors
raise RetryExhaustedException("api_call", attempts=3)
```

## Features

- ✅ Clean exception hierarchy
- ✅ Detailed error messages with optional details
- ✅ Framework-agnostic (works with FastAPI, Flask, Django, etc.)
- ✅ Type-safe
- ✅ Zero dependencies

## Exception Hierarchy

```
BaseApplicationException
├── BusinessLogicError
├── ValidationError
│   └── InvalidInputError
└── RetryExhaustedException
└── RetryableError
```

## License

MIT






