"""Unit tests for Pydantic field factories.

Tests email_field and token_field factory functions.
RULE: Maximum 100 lines per file.
"""

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_response_models.fields import email_field, token_field


class TestEmailField:
    """Tests for email_field factory."""

    def test_email_field_creates_field(self):
        """email_field should create a valid Pydantic field."""
        
        class TestModel(BaseModel):
            email: str = email_field()
        
        # Valid email should work
        model = TestModel(email="test@example.com")
        assert model.email == "test@example.com"

    def test_email_field_accepts_whitespace(self):
        """email_field accepts input (Pydantic v2 deprecated strip_whitespace)."""
        
        class TestModel(BaseModel):
            email: str = email_field()
        
        model = TestModel(email="  test@example.com  ")
        assert "test@example.com" in model.email

    def test_email_field_enforces_min_length(self):
        """email_field should enforce minimum length."""
        
        class TestModel(BaseModel):
            email: str = email_field()
        
        with pytest.raises(ValidationError):
            TestModel(email="ab")  # Too short (< 3 chars)

    def test_email_field_enforces_max_length(self):
        """email_field should enforce maximum length."""
        
        class TestModel(BaseModel):
            email: str = email_field()
        
        with pytest.raises(ValidationError):
            TestModel(email="a" * 300)  # Too long (> 255 chars)


class TestTokenField:
    """Tests for token_field factory."""

    def test_token_field_creates_field(self):
        """token_field should create a valid Pydantic field."""
        
        class TestModel(BaseModel):
            token: str = token_field()
        
        model = TestModel(token="abc123xyz")
        assert model.token == "abc123xyz"

    def test_token_field_accepts_whitespace(self):
        """token_field accepts input (Pydantic v2 deprecated strip_whitespace)."""
        
        class TestModel(BaseModel):
            token: str = token_field()
        
        model = TestModel(token="  mytoken  ")
        assert "mytoken" in model.token

    def test_token_field_enforces_min_length(self):
        """token_field should enforce minimum length."""
        
        class TestModel(BaseModel):
            token: str = token_field()
        
        with pytest.raises(ValidationError):
            TestModel(token="")  # Too short (< 1 char)

    def test_token_field_enforces_max_length(self):
        """token_field should enforce maximum length."""
        
        class TestModel(BaseModel):
            token: str = token_field()
        
        with pytest.raises(ValidationError):
            TestModel(token="a" * 300)  # Too long (> 255 chars)
