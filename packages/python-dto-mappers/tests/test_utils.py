"""Unit tests for mapping utility functions.

Tests extract_changed_fields and chain_map.
RULE: Maximum 100 lines per file.
"""

import pytest
from pydantic import BaseModel
from python_dto_mappers import extract_changed_fields, chain_map


class SampleUser(BaseModel):
    """Sample user model for testing."""
    id: int
    name: str
    email: str


class SampleUpdateDTO(BaseModel):
    """Sample update DTO for testing."""
    name: str
    email: str


def test_extract_changed_fields_with_changes():
    """Should extract only changed fields."""
    original = SampleUser(id=1, name="John", email="john@example.com")
    update = SampleUpdateDTO(name="Jane", email="john@example.com")
    
    changed = extract_changed_fields(original, update)
    
    assert changed == {"name": "Jane"}
    assert "email" not in changed


def test_extract_changed_fields_no_changes():
    """Should return empty dict when no changes."""
    original = SampleUser(id=1, name="John", email="john@example.com")
    update = SampleUpdateDTO(name="John", email="john@example.com")
    
    changed = extract_changed_fields(original, update)
    
    assert changed == {}


def test_extract_changed_fields_with_exclude():
    """Should exclude specified fields."""
    original = SampleUser(id=1, name="John", email="john@example.com")
    update = SampleUpdateDTO(name="Jane", email="jane@example.com")
    
    changed = extract_changed_fields(original, update, exclude={"email"})
    
    assert changed == {"name": "Jane"}
    assert "email" not in changed


def test_extract_changed_fields_all_changed():
    """Should extract all changed fields."""
    original = SampleUser(id=1, name="John", email="john@example.com")
    update = SampleUpdateDTO(name="Jane", email="jane@example.com")
    
    changed = extract_changed_fields(original, update)
    
    assert changed == {"name": "Jane", "email": "jane@example.com"}


def test_chain_map_with_pydantic():
    """Should chain map through Pydantic models."""
    
    class SourceModel(BaseModel):
        model_config = {"from_attributes": True}
        value: int
    
    class IntermediateModel(BaseModel):
        model_config = {"from_attributes": True}
        value: int
    
    class TargetModel(BaseModel):
        model_config = {"from_attributes": True}
        value: int
    
    source = SourceModel(value=42)
    result = chain_map(source, through=[IntermediateModel, TargetModel])
    
    assert isinstance(result, TargetModel)
    assert result.value == 42


def test_chain_map_single_step():
    """Should handle single mapping step."""
    
    class SourceModel(BaseModel):
        model_config = {"from_attributes": True}
        data: str
    
    class TargetModel(BaseModel):
        model_config = {"from_attributes": True}
        data: str
    
    source = SourceModel(data="test")
    result = chain_map(source, through=[TargetModel])
    
    assert isinstance(result, TargetModel)
    assert result.data == "test"
