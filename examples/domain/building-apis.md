# Domain Layer: Building APIs

Examples of building APIs using domain layer libraries for business logic, validation, and data handling.

## Example 1: FastAPI Application

Basic API endpoint with repositories, validation, sanitization, and error handling.

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Library imports
from python_app_exceptions import ValidationError, BusinessLogicError
from pydantic_response_models import SuccessResponse, ErrorResponse, PaginatedResponse
from sqlalchemy_async_repositories import BaseRepository
from python_technical_primitives.datetime import utc_now, add_days
from postgres_data_sanitizers import sanitize_dict_for_postgres
from python_input_validation import validate_email_format, sanitize_email

app = FastAPI()


# User Repository
class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)


# API Endpoint
@app.post("/users", response_model=SuccessResponse[UserResponse])
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Validate email
    if not validate_email_format(data.email):
        raise HTTPException(400, "Invalid email format")

    # Sanitize input
    email = sanitize_email(data.email)

    # Create user
    user = User(
        email=email,
        created_at=utc_now(),
        expires_at=add_days(utc_now(), 30)
    )

    # Sanitize JSONB data for PostgreSQL
    if data.metadata:
        user.metadata = sanitize_dict_for_postgres(data.metadata)

    # Save to database
    repo = UserRepository(db)
    saved_user = await repo.create(user)

    return SuccessResponse(data=UserResponse.from_orm(saved_user))


# Error handling
@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return ErrorResponse(
        error=exc.message,
        details=[{"field": exc.field, "message": str(exc)}]
    )


@app.exception_handler(BusinessLogicError)
async def business_error_handler(request, exc: BusinessLogicError):
    return ErrorResponse(error=exc.message)
```

## Example 7: Complete REST API

Full REST API with response models, pagination, validation, and sanitization.

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from pydantic_response_models import (
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse,
    email_field
)
from python_input_validation import validate_email_format, sanitize_email

app = FastAPI()


class UserCreate(BaseModel):
    email: str = email_field()
    name: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


@app.post("/users", response_model=SuccessResponse[UserResponse])
async def create_user(data: UserCreate):
    # Validate
    if not validate_email_format(data.email):
        raise HTTPException(400, "Invalid email")

    # Sanitize
    email = sanitize_email(data.email)

    # Create (mock)
    user = UserResponse(id=1, email=email, name=data.name)

    return SuccessResponse(
        data=user,
        message="User created successfully"
    )


@app.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(page: int = 1, page_size: int = 10):
    # Mock data
    users = [
        UserResponse(id=i, email=f"user{i}@example.com", name=f"User {i}")
        for i in range(1, 101)
    ]

    # Paginate
    start = (page - 1) * page_size
    end = start + page_size

    return PaginatedResponse(
        items=users[start:end],
        total=len(users),
        page=page,
        page_size=page_size,
        pages=(len(users) + page_size - 1) // page_size
    )
```
