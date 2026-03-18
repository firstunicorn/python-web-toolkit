"""Text case transformation utilities."""


def to_upper(text: str) -> str:
    """Convert text to uppercase.

    Args:
        text: Input string

    Returns:
        Uppercase string

    Example:
        >>> to_upper("hello")
        'HELLO'
    """
    return text.upper()


def to_lower(text: str) -> str:
    """Convert text to lowercase.

    Args:
        text: Input string

    Returns:
        Lowercase string

    Example:
        >>> to_lower("HELLO")
        'hello'
    """
    return text.lower()


def to_sentence_case(text: str) -> str:
    """Convert text to sentence case (first letter uppercase).

    Args:
        text: Input string

    Returns:
        Sentence case string

    Example:
        >>> to_sentence_case("hello world")
        'Hello world'
    """
    return text.capitalize() if text else text


def to_title_case(text: str) -> str:
    """Convert text to title case (each word capitalized).

    Args:
        text: Input string

    Returns:
        Title case string

    Example:
        >>> to_title_case("hello world")
        'Hello World'
    """
    return text.title()