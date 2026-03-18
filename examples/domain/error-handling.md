# Domain Layer: Error Handling

Examples of structured exception management using a clear hierarchy.

## Example 6: Exception Handling Hierarchy

Organized exception handling for validation errors, business logic violations, and application errors.

```python
from python_app_exceptions import (
    BaseApplicationException,
    ValidationError,
    BusinessLogicError,
    RetryExhaustedException
)

def create_user(email: str, age: int):
    # Validation errors
    if '@' not in email:
        raise ValidationError("email", email, "Invalid format")

    # Business rule violations
    if age < 18:
        raise BusinessLogicError(
            "user_must_be_adult",
            details=f"User is {age} years old"
        )

    # Success
    return {"email": email, "age": age}


# Catch specific exceptions
try:
    user = create_user("invalid", 16)
except ValidationError as e:
    print(f"Validation failed: {e.field} - {e.message}")
except BusinessLogicError as e:
    print(f"Business rule violated: {e.message}")
except BaseApplicationException as e:
    print(f"Application error: {e.message}")
```
