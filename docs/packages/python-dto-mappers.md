# python-dto-mappers

DTO mapping with type safety, auto-mapping, and field transformations.

## Installation

```bash
pip install python-dto-mappers
```

## Public API

| Symbol | Purpose |
|--------|---------|
| `Mapper[S, T]` | Protocol for type-safe mapping |
| `BaseMapper[S, T]` | Base mapper with type info |
| `AutoMapper` | Field-matching auto-mapper |
| `auto_map` decorator | Decorator for auto-mapping |
| `field_transform` decorator | Mark method as field transform |
| `extract_changed_fields(original, update)` | PATCH partial updates |
| `chain_map(source, through)` | Chain multiple mappings |

### field mappers

| Function | Purpose |
|----------|---------|
| `map_datetime_to_iso(dt)` | datetime to ISO string |
| `map_iso_to_datetime(s)` | ISO string to datetime |
| `map_nested_object(obj, mapper)` | Map nested objects |
| `to_upper/to_lower/to_sentence_case/to_title_case` | Text transforms |

## Usage

```python
from python_dto_mappers import AutoMapper

mapper = AutoMapper(UserEntity, UserDTO)
dto = mapper.map(entity)
```
