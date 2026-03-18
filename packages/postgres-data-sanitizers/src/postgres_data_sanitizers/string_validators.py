"""Shared string validation utilities."""


def contains_surrogates(text: str) -> bool:
    """Check if string contains UTF-8 surrogate characters.

    Surrogates (U+D800 to U+DFFF) are invalid in UTF-8 and rejected by PostgreSQL.

    Args:
        text: String to validate

    Returns:
        True if string contains surrogate characters, False otherwise
    """
    if not text:
        return False
    try:
        # Try to encode as UTF-8; surrogates will raise UnicodeEncodeError
        text.encode('utf-8', errors='strict')
        return False
    except UnicodeEncodeError:
        return True






