"""String utility operations."""
import re
from typing import Optional


def to_sentence_case(text: str) -> str:
    """Convert string to sentence case (first letter capitalized)."""
    if not text:
        return text
    return text[0].upper() + text[1:].lower()


def to_lower_case(text: str) -> str:
    """Convert string to lowercase."""
    return text.lower()


def to_upper_case(text: str) -> str:
    """Convert string to uppercase."""
    return text.upper()


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to max length with suffix.

    Args:
        text: String to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace (collapse multiple spaces to single)."""
    return ' '.join(text.split())


def is_valid_email(email: str) -> bool:
    """Check if string is valid email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing/replacing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for file systems
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    return filename or 'unnamed'


def extract_extension(filename: str) -> Optional[str]:
    """Extract file extension from filename."""
    if '.' not in filename:
        return None
    return filename.rsplit('.', 1)[1].lower()






