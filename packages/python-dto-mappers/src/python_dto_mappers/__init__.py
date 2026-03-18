"""Python DTO Mappers - Reusable DTO mapping patterns."""

from python_dto_mappers.base import Mapper, BaseMapper
from python_dto_mappers.auto_mapper import AutoMapper
from python_dto_mappers.decorators import auto_map, field_transform
from python_dto_mappers.field_mappers import (
    to_upper,
    to_lower,
    to_sentence_case,
    to_title_case,
    map_datetime_to_iso,
    map_iso_to_datetime,
    map_nested_object,
)
from python_dto_mappers.utils import extract_changed_fields, chain_map

__version__ = "0.1.0"

__all__ = [
    "Mapper",
    "BaseMapper",
    "AutoMapper",
    "auto_map",
    "field_transform",
    "to_upper",
    "to_lower",
    "to_sentence_case",
    "to_title_case",
    "map_datetime_to_iso",
    "map_iso_to_datetime",
    "map_nested_object",
    "extract_changed_fields",
    "chain_map",
]
