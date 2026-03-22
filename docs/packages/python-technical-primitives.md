# python-technical-primitives

General-purpose Python utilities: datetime operations, text processing, specification pattern.

## Installation

```bash
pip install python-technical-primitives
```

## Public API

### datetime operations

| Function | Purpose |
|----------|---------|
| `utc_now()` | Current UTC datetime with tzinfo |
| `add_days(dt, days)` | Add days to datetime |
| `add_hours(dt, hours)` | Add hours to datetime |
| `is_expired(expiry_dt)` | Check if datetime has passed |
| `days_until(target_dt)` | Days until target |
| `to_iso_string(dt)` / `from_iso_string(s)` | ISO 8601 conversion |

### text operations

| Function | Purpose |
|----------|---------|
| `to_sentence_case(text)` | Sentence case conversion |
| `truncate(text, max_length)` | Truncate with suffix |
| `normalize_whitespace(text)` | Collapse whitespace |
| `is_valid_email(email)` | Email format check |
| `sanitize_filename(filename)` | Remove invalid chars |
| `extract_extension(filename)` | Get file extension |

### specification pattern

| Class | Purpose |
|-------|---------|
| `Specification[T]` | Base specification (composable with `&`, `\|`, `~`) |
| `AndSpecification` | Both specs satisfied |
| `OrSpecification` | At least one satisfied |
| `NotSpecification` | Spec not satisfied |
