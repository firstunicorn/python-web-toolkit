"""Auto-mapping engine for matching fields between models."""

from typing import Type, Set, Optional, Any


class AutoMapper:
    """Class-based auto-mapper for matching fields.

    Automatically maps fields with matching names between source
    and target Pydantic models. Custom transforms override auto-mapping.

    Example:
        >>> mapper = AutoMapper(UserORM, UserDTO, exclude={'internal_id'})
        >>> dto = mapper.map(user_orm)
    """

    def __init__(
        self,
        source_type: Type,
        target_type: Type,
        exclude: Optional[Set[str]] = None
    ):
        self._source_type = source_type
        self._target_type = target_type
        self._exclude = exclude or set()
        self._transforms = {}
        self._matching_fields = self._compute_matching_fields()

    def _compute_matching_fields(self) -> Set[str]:
        """Compute intersection of source and target fields."""
        source_fields = set(self._source_type.model_fields.keys())
        target_fields = set(self._target_type.model_fields.keys())
        return (source_fields & target_fields) - self._exclude

    def add_transform(self, field: str, func: Any) -> "AutoMapper":
        """Register a custom transform for a field.

        Args:
            field: Field name to transform
            func: Callable(source) -> value

        Returns:
            Self for chaining
        """
        self._transforms[field] = func
        return self

    def map(self, source: Any) -> Any:
        """Map source instance to target type.

        Args:
            source: Source model instance

        Returns:
            Target model instance with mapped fields
        """
        data = {}
        for field in self._matching_fields:
            if field in self._transforms:
                data[field] = self._transforms[field](source)
            else:
                data[field] = getattr(source, field)
        return self._target_type(**data)

    @property
    def source_type(self) -> Type:
        """Source model type."""
        return self._source_type

    @property
    def target_type(self) -> Type:
        """Target model type."""
        return self._target_type

    @property
    def mapped_fields(self) -> Set[str]:
        """Set of fields being mapped."""
        return self._matching_fields.copy()
