# pydantic-response-models

Standard API response DTOs using Pydantic (framework-agnostic).

## Installation

```bash
pip install pydantic-response-models
```

## Usage

```python
from pydantic_response_models import (
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse,
    MessageResponse,
    email_field,
    token_field
)
from pydantic import BaseModel

# Success response
response = SuccessResponse(data={"id": 1, "name": "John"})

# Error response
error = ErrorResponse(error="Not found", code="404")

# Paginated response
paginated = PaginatedResponse(
    items=[...],
    total=100,
    page=1,
    page_size=20,
    pages=5
)

# Use field factories in your models
class LoginRequest(BaseModel):
    email: str = email_field()
    token: str = token_field()
```

## Features

- ✅ Generic response wrappers
- ✅ Type-safe with Pydantic
- ✅ Framework-agnostic (works with FastAPI, Flask, Django, etc.)
- ✅ Consistent field definitions
- ✅ Pagination support

## License

MIT






