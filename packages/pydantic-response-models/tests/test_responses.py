"""Unit tests for API response models.

Tests SuccessResponse, ErrorResponse, PaginatedResponse, and MessageResponse.
RULE: Maximum 100 lines per file.
"""

import pytest
from pydantic import ValidationError

from pydantic_response_models import (
    SuccessResponse,
    ErrorResponse,
    ErrorDetail,
    PaginatedResponse,
    MessageResponse,
)


class TestSuccessResponse:
    """Tests for SuccessResponse model."""

    def test_success_response_with_data(self):
        """SuccessResponse should serialize data correctly."""
        response = SuccessResponse(data={"id": 1, "name": "Test"})
        assert response.success is True
        assert response.data == {"id": 1, "name": "Test"}
        assert response.message is None

    def test_success_response_with_message(self):
        """SuccessResponse should accept optional message."""
        response = SuccessResponse(data="done", message="Operation completed")
        assert response.success is True
        assert response.message == "Operation completed"

    def test_success_response_serialization(self):
        """SuccessResponse should serialize to dict correctly."""
        response = SuccessResponse(data=[1, 2, 3])
        data = response.model_dump()
        assert data["success"] is True
        assert data["data"] == [1, 2, 3]


class TestErrorResponse:
    """Tests for ErrorResponse model."""

    def test_error_response_basic(self):
        """ErrorResponse should accept error message."""
        response = ErrorResponse(error="Something went wrong")
        assert response.success is False
        assert response.error == "Something went wrong"
        assert response.details is None

    def test_error_response_with_details(self):
        """ErrorResponse should accept error details."""
        detail = ErrorDetail(field="email", message="Invalid format", code="INVALID_EMAIL")
        response = ErrorResponse(error="Validation failed", details=[detail])
        assert len(response.details) == 1
        assert response.details[0].field == "email"

    def test_error_response_with_code(self):
        """ErrorResponse should accept error code."""
        response = ErrorResponse(error="Not found", code="NOT_FOUND_404")
        assert response.code == "NOT_FOUND_404"


class TestPaginatedResponse:
    """Tests for PaginatedResponse model."""

    def test_paginated_response_basic(self):
        """PaginatedResponse should handle pagination metadata."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            total=10,
            page=1,
            page_size=3,
            pages=4
        )
        assert len(response.items) == 3
        assert response.total == 10
        assert response.pages == 4

    def test_paginated_response_empty_items(self):
        """PaginatedResponse should handle empty results."""
        response = PaginatedResponse(items=[], total=0, page=1, page_size=10, pages=0)
        assert response.items == []
        assert response.total == 0


class TestMessageResponse:
    """Tests for MessageResponse model."""

    def test_message_response_basic(self):
        """MessageResponse should accept message."""
        response = MessageResponse(message="Operation successful")
        assert response.message == "Operation successful"
        assert response.success is True

    def test_message_response_failure(self):
        """MessageResponse should allow success=False."""
        response = MessageResponse(message="Failed", success=False)
        assert response.success is False
