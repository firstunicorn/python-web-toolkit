# python-technical-primitives

General-purpose Python utilities (datetime, text, patterns).

## Installation

```bash
pip install python-technical-primitives
```

## Usage

### Datetime Utilities

```python
from python_technical_primitives.datetime import utc_now, add_days, is_expired

now = utc_now()
future = add_days(now, 7)
expired = is_expired(now)  # False
```

### Text Utilities

```python
from python_technical_primitives.text import to_snake_case, sanitize_filename

snake = to_snake_case("HelloWorld")  # "hello_world"
safe = sanitize_filename("my file?.txt")  # "my_file.txt"
```

### Specification Pattern

```python
from python_technical_primitives.patterns import Specification

class AdultSpec(Specification[User]):
    description = "User must be 18+"
    def is_satisfied_by(self, user):
        return user.age >= 18

class VerifiedSpec(Specification[User]):
    description = "User must be verified"
    def is_satisfied_by(self, user):
        return user.verified

# Combine specifications
spec = AdultSpec() & VerifiedSpec()
if spec(user):
    print("User is adult and verified")
else:
    print(f"Errors: {spec.errors}")
```

## Features

- ✅ Zero dependencies
- ✅ Framework-agnostic
- ✅ Type-safe
- ✅ Well-tested utilities

## License

MIT






