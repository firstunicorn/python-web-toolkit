# Python DTO Mappers

Reusable DTO mapping patterns with type safety and auto-mapping functionality.

## Installation

```bash
pip install python-dto-mappers
```

## Features

- **BaseMapper Protocol**: Type-safe mapper interface
- **Auto-Mapping**: Automatic field mapping with @auto_map decorator
- **Field Transformations**: Common transformations (snake_case ↔ camelCase, datetime ↔ ISO)
- **Partial Updates**: Extract changed fields for PATCH operations
- **Chained Mapping**: ORM → Domain → DTO transformations

## Usage

### Basic Mapper

```python
from pydantic import BaseModel
from python_dto_mappers import BaseMapper

class UserEntity(BaseModel):
    id: int
    name: str
    email: str

class UserDTO(BaseModel):
    id: int
    name: str
    email: str

class UserMapper(BaseMapper[UserEntity, UserDTO]):
    def map(self, source: UserEntity) -> UserDTO:
        return UserDTO(
            id=source.id,
            name=source.name,
            email=source.email
        )
```

### Auto-Mapping

```python
from python_dto_mappers import auto_map

@auto_map(UserEntity, UserDTO)
class UserAutoMapper:
    def transform_name(self, source):
        # Custom transformation for specific field
        return source.name.upper()

mapper = UserAutoMapper()
dto = mapper.map(user_entity)
```

### Field Transformations

```python
from python_dto_mappers import snake_to_camel, map_datetime_to_iso

# Case conversion
camel = snake_to_camel("user_name")  # "userName"
snake = camel_to_snake("userName")   # "user_name"

# Datetime conversion
iso_str = map_datetime_to_iso(datetime.now())
dt = map_iso_to_datetime("2024-01-01T12:00:00")
```

### Partial Updates (PATCH)

```python
from python_dto_mappers import extract_changed_fields

original = User(id=1, name="John", email="john@example.com")
update = UserUpdateDTO(name="Jane", email="john@example.com")

changed = extract_changed_fields(original, update)
# {'name': 'Jane'} - only changed fields
```

### Chained Mapping

```python
from python_dto_mappers import chain_map

# ORM → Domain → DTO
dto = chain_map(
    orm_user,
    through=[DomainUser, UserDTO]
)
```

## API Reference

### `Mapper[TSource, TTarget]` (Protocol)

Type-safe mapper protocol.

### `BaseMapper[TSource, TTarget]`

Base mapper class with type information.

### `@auto_map(source_type, target_type, exclude=None)`

Auto-generate mapping for matching fields.

**Parameters:**
- `source_type`: Source model type
- `target_type`: Target model type
- `exclude`: Set of fields to exclude

### `@field_transform(field_name)`

Mark method as field transformation.

### Field Transformers

- `snake_to_camel(snake_str)`: snake_case → camelCase
- `camel_to_snake(camel_str)`: camelCase → snake_case
- `map_datetime_to_iso(dt)`: datetime → ISO string
- `map_iso_to_datetime(iso_str)`: ISO string → datetime
- `map_nested_object(obj, mapper)`: Map nested object

### Utils

- `extract_changed_fields(original, update_dto, exclude)`: Extract changed fields
- `chain_map(source, through)`: Chain multiple mappings

## Dependencies

- `pydantic>=2.0.0`
- `typing-extensions>=4.0.0`

## License

MIT
