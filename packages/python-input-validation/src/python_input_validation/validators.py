"""Business-level input validators."""
import re
from typing import Optional


def validate_email_format(email: str) -> bool:
    """
    Validate email format (business-level).

    Args:
        email: Email to validate

    Returns:
        True if valid format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_string_length(
    text: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> bool:
    """
    Validate string length constraints.

    Args:
        text: Text to validate
        min_length: Minimum length (inclusive)
        max_length: Maximum length (inclusive)

    Returns:
        True if length is valid
    """
    length = len(text)
    if min_length is not None and length < min_length:
        return False
    if max_length is not None and length > max_length:
        return False
    return True






