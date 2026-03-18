"""Validation functions for PostgreSQL text fields.

RULE: Maximum 100 lines per file.
"""

from typing import Optional

from .escape import escape_null_chars


def validate_postgres_text(text: Optional[str]) -> Optional[str]:
    """Validate and escape text for PostgreSQL storage.

    Escapes null characters (preserving data integrity).

    Args:
        text: Input text to validate

    Returns:
        Escaped text safe for PostgreSQL or None if input was None
    """
    if text is None:
        return None

    if '\x00' in text:
        # **CRITICAL**: Log this for monitoring in production
        # TODO: Add proper logging when logger is available
        return escape_null_chars(text)

    return text






