"""Decorators for auto-mapping (syntactic sugar over AutoMapper)."""

from typing import Type, Set, Optional, Callable
from python_dto_mappers.auto_mapper import AutoMapper


def auto_map(
    source_type: Type,
    target_type: Type,
    exclude: Optional[Set[str]] = None
) -> Callable:
    """Decorator to auto-generate mapping for matching fields.

    Uses AutoMapper engine under the hood. Custom transforms
    can be defined with transform_{field_name} methods on the class.

    Args:
        source_type: Source model type
        target_type: Target model type
        exclude: Set of field names to exclude from auto-mapping

    Returns:
        Class decorator function

    Example:
        >>> @auto_map(UserEntity, UserDTO, exclude={'id'})
        ... class UserMapper:
        ...     def transform_name(self, source):
        ...         return source.name.upper()
    """
    def decorator(cls):
        mapper = AutoMapper(source_type, target_type, exclude)

        # Register transform methods from decorated class
        for attr_name in dir(cls):
            if attr_name.startswith("transform_"):
                field_name = attr_name[len("transform_"):]
                method = getattr(cls, attr_name)
                mapper.add_transform(field_name, method)

        def map_func(self, source):
            """Auto-generated mapping function."""
            return mapper.map(source)

        cls.map = map_func
        cls._auto_mapper = mapper
        return cls

    return decorator


def field_transform(field_name: str) -> Callable:
    """Mark a method as a field transformation.

    Args:
        field_name: Name of the field this transforms

    Returns:
        Method decorator

    Example:
        >>> @field_transform("created_at")
        ... def transform_date(self, source):
        ...     return source.created_at.isoformat()
    """
    def decorator(func):
        func._field_transform = field_name
        return func
    return decorator
