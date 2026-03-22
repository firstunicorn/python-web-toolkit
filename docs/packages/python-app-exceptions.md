# python-app-exceptions

Typed exception hierarchy for application/business logic errors.

## Installation

```bash
pip install python-app-exceptions
```

## Public API

| Exception | Purpose |
|-----------|---------|
| `BaseApplicationException` | Root for all app errors (`message`, `details`) |
| `BusinessLogicError` | Business rule violations (`rule`, `details`) |
| `ValidationError` | Data validation failures (`field`, `value`) |
| `InvalidInputError` | Invalid input format (`input_name`, `expected_format`) |
| `RetryExhaustedException` | All retry attempts failed (`operation`, `attempts`) |
| `RetryableError` | Transient error, can retry (`message`, `retry_after`) |

## Usage

```python
from python_app_exceptions import BusinessLogicError, ValidationError

raise BusinessLogicError(rule="email_unique", details={"email": email})
raise ValidationError(field="age", value=-1, details={"constraint": "positive"})
```

See also: [exception libraries comparison](../exception-comparison)
