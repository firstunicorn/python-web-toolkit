"""Unit tests for base mapper classes.

Tests Mapper protocol and BaseMapper class.
RULE: Maximum 100 lines per file.
"""

import pytest
from python_dto_mappers import BaseMapper


class SourceModel:
    """Sample source model for testing."""
    def __init__(self, value: int):
        self.value = value


class TargetModel:
    """Sample target model for testing."""
    def __init__(self, value: int):
        self.value = value


def test_base_mapper_initialization():
    """Should initialize with source and target types."""
    mapper = BaseMapper(SourceModel, TargetModel)
    
    assert mapper.source_type == SourceModel
    assert mapper.target_type == TargetModel


def test_base_mapper_map_not_implemented():
    """Should raise NotImplementedError for unimplemented map."""
    mapper = BaseMapper(SourceModel, TargetModel)
    source = SourceModel(42)
    
    with pytest.raises(NotImplementedError, match="must implement map"):
        mapper.map(source)


def test_base_mapper_custom_implementation():
    """Should allow custom mapper implementation."""
    
    class CustomMapper(BaseMapper[SourceModel, TargetModel]):
        def map(self, source: SourceModel) -> TargetModel:
            return TargetModel(value=source.value * 2)
    
    mapper = CustomMapper(SourceModel, TargetModel)
    source = SourceModel(21)
    result = mapper.map(source)
    
    assert isinstance(result, TargetModel)
    assert result.value == 42


def test_base_mapper_preserves_type_info():
    """Should preserve type information for generic usage."""
    
    class ConcreteMapper(BaseMapper[SourceModel, TargetModel]):
        def map(self, source: SourceModel) -> TargetModel:
            return TargetModel(value=source.value)
    
    mapper = ConcreteMapper(SourceModel, TargetModel)
    
    assert mapper.source_type.__name__ == "SourceModel"
    assert mapper.target_type.__name__ == "TargetModel"


def test_base_mapper_identity_mapping():
    """Should support identity mapping (same type in/out)."""
    
    class IdentityMapper(BaseMapper[SourceModel, SourceModel]):
        def map(self, source: SourceModel) -> SourceModel:
            return SourceModel(value=source.value)
    
    mapper = IdentityMapper(SourceModel, SourceModel)
    source = SourceModel(100)
    result = mapper.map(source)
    
    assert isinstance(result, SourceModel)
    assert result.value == 100
