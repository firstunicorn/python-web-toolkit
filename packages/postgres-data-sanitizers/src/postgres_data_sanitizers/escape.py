"""Core null character escaping for PostgreSQL compatibility.

RULE: Maximum 100 lines per file.
"""


def escape_null_chars(text: str) -> str:
    """Escape null characters to Unicode representation for PostgreSQL.

    **CRITICAL**: PostgreSQL rejects \u0000 (null character) in TEXT/VARCHAR fields.
    This was discovered by property-based testing causing:
        asyncpg.exceptions.UntranslatableCharacterError

    This function ESCAPES null characters instead of removing them,
    preserving data integrity. Use unescape_null_chars() to restore.

    Args:
        text: Input string that may contain null characters

    Returns:
        String with null characters escaped as literal "\\u0000"

    Example:
        >>> escape_null_chars("hello\x00world")
        'hello\\\\u0000world'
    """
    return text.replace('\x00', '\\u0000')


def unescape_null_chars(text: str) -> str:
    """Unescape Unicode representation back to null characters.

    Reverses the escaping done by escape_null_chars().

    Args:
        text: String with escaped null characters

    Returns:
        String with literal "\\u0000" converted back to \x00

    Example:
        >>> unescape_null_chars("hello\\\\u0000world")
        'hello\x00world'
    """
    return text.replace('\\u0000', '\x00')






