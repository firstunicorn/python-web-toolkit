"""Dictionary sanitization for PostgreSQL JSONB compatibility.

RULE: Maximum 100 lines per file.
"""

from typing import Any, Dict

from .escape import escape_null_chars, unescape_null_chars


def sanitize_dict_for_postgres(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively escape null chars in dict for PostgreSQL JSONB storage.

    **CRITICAL**: Prevents database crashes from null characters in JSON.
    Escapes null characters instead of removing them, preserving data.

    Args:
        data: Dictionary that may contain null characters in strings

    Returns:
        Sanitized dictionary safe for PostgreSQL JSONB (data preserved)
    """
    if not isinstance(data, dict):
        return data

    sanitized = {}
    for key, value in data.items():
        # Escape null chars in key
        clean_key = escape_null_chars(key) if isinstance(key, str) else key

        # Escape value recursively
        if isinstance(value, str):
            sanitized[clean_key] = escape_null_chars(value)
        elif isinstance(value, dict):
            sanitized[clean_key] = sanitize_dict_for_postgres(value)
        elif isinstance(value, list):
            sanitized[clean_key] = [
                sanitize_dict_for_postgres(item) if isinstance(item, dict)
                else escape_null_chars(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            sanitized[clean_key] = value

    return sanitized


def unescape_dict_from_postgres(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively unescape null chars from PostgreSQL JSONB data.

    Reverses the escaping done by sanitize_dict_for_postgres().

    Args:
        data: Dictionary with escaped null characters

    Returns:
        Dictionary with null characters restored
    """
    if not isinstance(data, dict):
        return data

    unescaped = {}
    for key, value in data.items():
        # Unescape null chars in key
        clean_key = unescape_null_chars(key) if isinstance(key, str) else key

        # Unescape value recursively
        if isinstance(value, str):
            unescaped[clean_key] = unescape_null_chars(value)
        elif isinstance(value, dict):
            unescaped[clean_key] = unescape_dict_from_postgres(value)
        elif isinstance(value, list):
            unescaped[clean_key] = [
                unescape_dict_from_postgres(item) if isinstance(item, dict)
                else unescape_null_chars(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            unescaped[clean_key] = value

    return unescaped






