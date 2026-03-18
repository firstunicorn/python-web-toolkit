# Domain Layer: Data Patterns

Examples of domain modeling, business rules, and data sanitization patterns.

## Example 2: Domain Model with Specification Pattern

Composable business rules using the Specification pattern for complex validation logic.

```python
from dataclasses import dataclass
from python_technical_primitives.patterns import Specification
from python_technical_primitives.datetime import utc_now

@dataclass
class User:
    email: str
    age: int
    verified: bool
    created_at: datetime


class AdultUserSpec(Specification[User]):
    """User must be 18 or older."""
    description = "User must be 18+"

    def is_satisfied_by(self, user: User) -> bool:
        if user.age < 18:
            self._add_error()
            return False
        return True


class VerifiedEmailSpec(Specification[User]):
    """User must have verified email."""
    description = "Email must be verified"

    def is_satisfied_by(self, user: User) -> bool:
        if not user.verified:
            self._add_error()
            return False
        return True


class ActiveUserSpec(Specification[User]):
    """User account must be recently active (30 days)."""
    description = "Account must be active (last 30 days)"

    def is_satisfied_by(self, user: User) -> bool:
        thirty_days_ago = add_days(utc_now(), -30)
        if user.created_at < thirty_days_ago:
            self._add_error()
            return False
        return True


# Combine specifications
eligible_user_spec = AdultUserSpec() & VerifiedEmailSpec() & ActiveUserSpec()

# Use specification
user = User(email="user@example.com", age=25, verified=True, created_at=utc_now())

if eligible_user_spec(user):
    print("User is eligible!")
else:
    print(f"User not eligible: {eligible_user_spec.errors}")
```

## Example 3: Data Sanitization Pipeline

Multi-stage sanitization pipeline for PostgreSQL-safe data processing.

```python
from postgres_data_sanitizers import (
    sanitize_dict_for_postgres,
    escape_null_chars,
    validate_postgres_text
)
from python_input_validation import sanitize_text_input

def process_user_input(data: dict) -> dict:
    """Process and sanitize user input before database storage."""

    # Step 1: Sanitize text fields
    if 'name' in data:
        data['name'] = sanitize_text_input(data['name'], max_length=100)

    if 'bio' in data:
        data['bio'] = sanitize_text_input(data['bio'], max_length=500)

    # Step 2: Validate and escape for PostgreSQL
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = validate_postgres_text(value)

    # Step 3: Sanitize nested structures for JSONB
    if 'metadata' in data and isinstance(data['metadata'], dict):
        data['metadata'] = sanitize_dict_for_postgres(data['metadata'])

    return data


# Example usage
user_data = {
    "name": "  John Doe  ",
    "bio": "Software engineer\x00with experience",  # Null char!
    "metadata": {
        "preferences": {
            "theme": "dark\x00mode",  # Null char in nested dict!
            "notifications": True
        }
    }
}

clean_data = process_user_input(user_data)
# Now safe for PostgreSQL!
```
