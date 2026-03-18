"""Mapping utilities for partial updates and chaining."""

from typing import Any, Dict, List, Type, Optional, Set
from pydantic import BaseModel


def extract_changed_fields(
    original: BaseModel,
    update_dto: BaseModel,
    exclude: Optional[Set[str]] = None
) -> Dict[str, Any]:
    """Extract only changed fields for partial updates (PATCH).
    
    Compares original object with update DTO and returns only fields
    that have changed. Useful for HTTP PATCH operations.
    
    Args:
        original: Original object
        update_dto: Update DTO with new values
        exclude: Fields to exclude from comparison
    
    Returns:
        Dictionary with only changed fields
    
    Example:
        >>> original = User(id=1, name="John", email="john@example.com")
        >>> update = UserUpdateDTO(name="Jane", email="john@example.com")
        >>> changed = extract_changed_fields(original, update)
        >>> # {'name': 'Jane'}
    """
    exclude = exclude or set()
    changed = {}
    
    for field in update_dto.model_fields:
        if field in exclude:
            continue
        
        new_value = getattr(update_dto, field, None)
        old_value = getattr(original, field, None)
        
        if new_value is not None and new_value != old_value:
            changed[field] = new_value
    
    return changed


def chain_map(source: Any, through: List[Type]) -> Any:
    """Chain multiple mappings in sequence.
    
    Applies multiple type transformations in order, useful for
    ORM → Domain → DTO conversions.
    
    Args:
        source: Source object to map
        through: List of target types to map through
    
    Returns:
        Final mapped object
    
    Example:
        >>> # ORM → Domain → DTO
        >>> dto = chain_map(
        ...     orm_user,
        ...     through=[DomainUser, UserDTO]
        ... )
    """
    result = source
    
    for target_type in through:
        # Try different mapping methods
        if hasattr(target_type, 'from_orm'):
            result = target_type.from_orm(result)
        elif hasattr(target_type, 'model_validate'):
            result = target_type.model_validate(result)
        elif hasattr(result, f'to_{target_type.__name__.lower()}'):
            # Call custom conversion method
            method_name = f'to_{target_type.__name__.lower()}'
            result = getattr(result, method_name)()
        else:
            raise ValueError(
                f"Cannot map {type(result).__name__} to {target_type.__name__}"
            )
    
    return result
