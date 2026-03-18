"""Business-level input sanitizers."""
from typing import Optional


def sanitize_email(email: str) -> str:
    """
    Sanitize email input (business-level).

    Args:
        email: Email address to sanitize

    Returns:
        Sanitized email (lowercased, trimmed)
    """
    return email.strip().lower()


def sanitize_text_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize general text input.

    Args:
        text: Text to sanitize
        max_length: Optional maximum length

    Returns:
        Sanitized text
    """
    text = text.strip()
    if max_length and len(text) > max_length:
        text = text[:max_length]
    return text






