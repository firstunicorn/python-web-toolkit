"""Nested object mapping utilities."""

from typing import Any


def map_nested_object(obj: Any, mapper: 'Mapper') -> Any:
    """Map nested object using provided mapper.
    
    Args:
        obj: Object to map or None
        mapper: Mapper instance with map() method
    
    Returns:
        Mapped object or None
    
    Example:
        >>> address_mapper = AddressMapper()
        >>> mapped = map_nested_object(user.address, address_mapper)
    """
    if obj is None:
        return None
    return mapper.map(obj)
