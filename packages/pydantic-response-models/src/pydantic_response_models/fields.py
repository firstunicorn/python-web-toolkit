"""Universal field factory functions for Pydantic models."""

from pydantic import Field


def email_field() -> Field:
    """Factory for email field."""
    return Field(
        ...,
        description="Email address",
        min_length=3,
        max_length=255,
        strip_whitespace=True
    )


def token_field() -> Field:
    """Factory for token field with consistent definition."""
    return Field(
        ...,
        description="Secure random token",
        min_length=1,
        max_length=255,
        strip_whitespace=True
    )






