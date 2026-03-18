"""Query model for count use case."""

from pydantic import BaseModel


class CountQuery(BaseModel):
    """Query: Count total entities."""
    pass  # No parameters needed for basic count

