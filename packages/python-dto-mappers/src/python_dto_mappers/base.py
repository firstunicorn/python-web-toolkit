"""Base mapper protocol and class."""

from typing import Protocol, TypeVar, Generic, Type

TSource = TypeVar('TSource')
TTarget = TypeVar('TTarget')


class Mapper(Protocol[TSource, TTarget]):
    """Protocol for type-safe mapping between types.
    
    Use this protocol to define mappers with type safety.
    
    Example:
        >>> class UserMapper(Mapper[UserEntity, UserDTO]):
        ...     def map(self, source: UserEntity) -> UserDTO:
        ...         return UserDTO(id=source.id, name=source.name)
    """
    
    def map(self, source: TSource) -> TTarget:
        """Map source object to target type.
        
        Args:
            source: Source object to map
            
        Returns:
            Mapped target object
        """
        ...


class BaseMapper(Generic[TSource, TTarget]):
    """Base mapper with common functionality.
    
    Extend this class to create concrete mappers with type information.
    
    Example:
        >>> class UserMapper(BaseMapper[UserEntity, UserDTO]):
        ...     def map(self, source: UserEntity) -> UserDTO:
        ...         return UserDTO(id=source.id, name=source.name)
    """
    
    def __init__(
        self,
        source_type: Type[TSource],
        target_type: Type[TTarget]
    ):
        """Initialize mapper with type information.
        
        Args:
            source_type: Source type class
            target_type: Target type class
        """
        self.source_type = source_type
        self.target_type = target_type
    
    def map(self, source: TSource) -> TTarget:
        """Map source to target.
        
        Override in subclasses to implement mapping logic.
        
        Args:
            source: Source object
            
        Returns:
            Mapped target object
            
        Raises:
            NotImplementedError: If not overridden in subclass
        """
        raise NotImplementedError(
            f"Mapper for {self.source_type} -> {self.target_type} "
            "must implement map() method"
        )
