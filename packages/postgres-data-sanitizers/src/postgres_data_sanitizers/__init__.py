"""PostgreSQL data sanitizers library."""

from .escape import escape_null_chars, unescape_null_chars
from .sanitize import sanitize_dict_for_postgres, unescape_dict_from_postgres
from .validate import validate_postgres_text
from .string_validators import contains_surrogates

__version__ = "0.1.0"

__all__ = [
    "escape_null_chars",
    "unescape_null_chars",
    "sanitize_dict_for_postgres",
    "unescape_dict_from_postgres",
    "validate_postgres_text",
    "contains_surrogates",
]






