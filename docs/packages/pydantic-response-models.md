# pydantic-response-models

Standard API response DTOs using Pydantic. Framework-agnostic.

## Installation

```bash
pip install pydantic-response-models
```

## Public API

| Class | Purpose |
|-------|---------|
| `SuccessResponse[T]` | Generic success wrapper (`data: T`, `message`) |
| `ErrorDetail` | Error detail model (`field`, `message`, `code`) |
| `ErrorResponse` | Standard error response (`errors: List[ErrorDetail]`) |
| `PaginatedResponse[T]` | Pagination wrapper (`items`, `total`, `page`, `page_size`) |
| `MessageResponse` | Simple message DTO |

### Field factories

| Function | Purpose |
|----------|---------|
| `email_field()` | Pydantic `Field` for email |
| `token_field()` | Pydantic `Field` for tokens |

## Usage

```python
from pydantic_response_models import SuccessResponse, PaginatedResponse

response = SuccessResponse(data={"id": 1}, message="created")
paginated = PaginatedResponse(items=[...], total=50, page=1, page_size=10)
```
