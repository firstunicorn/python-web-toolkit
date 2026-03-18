"""Datetime to/from ISO 8601 string conversions."""

from typing import Optional
from datetime import datetime


def map_datetime_to_iso(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO 8601 string.
    
    Args:
        dt: Datetime object or None
    
    Returns:
        ISO 8601 formatted string or None
    
    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2024, 1, 1, 12, 0, 0)
        >>> map_datetime_to_iso(dt)
        '2024-01-01T12:00:00'
    """
    return dt.isoformat() if dt else None


def map_iso_to_datetime(iso_str: Optional[str]) -> Optional[datetime]:
    """Convert ISO 8601 string to datetime.
    
    Args:
        iso_str: ISO 8601 formatted string or None
    
    Returns:
        Datetime object or None
    
    Example:
        >>> map_iso_to_datetime("2024-01-01T12:00:00")
        datetime.datetime(2024, 1, 1, 12, 0)
    """
    return datetime.fromisoformat(iso_str) if iso_str else None
