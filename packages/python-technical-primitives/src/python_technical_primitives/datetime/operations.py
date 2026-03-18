"""Date/time utility operations."""
from datetime import datetime, timedelta, timezone
from typing import Optional


def utc_now() -> datetime:
    """Get current UTC datetime with timezone info."""
    return datetime.now(timezone.utc)


def add_days(dt: datetime, days: int) -> datetime:
    """Add days to datetime."""
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """Add hours to datetime."""
    return dt + timedelta(hours=hours)


def is_expired(expiry_dt: datetime, reference_dt: Optional[datetime] = None) -> bool:
    """
    Check if expiry datetime has passed.

    Args:
        expiry_dt: The expiration datetime to check
        reference_dt: Reference datetime (defaults to now)

    Returns:
        True if expired, False otherwise
    """
    if reference_dt is None:
        reference_dt = utc_now()
    return expiry_dt <= reference_dt


def days_until(target_dt: datetime, reference_dt: Optional[datetime] = None) -> int:
    """
    Calculate days until target datetime.

    Args:
        target_dt: Target datetime
        reference_dt: Reference datetime (defaults to now)

    Returns:
        Number of days (negative if past)
    """
    if reference_dt is None:
        reference_dt = utc_now()
    delta = target_dt - reference_dt
    return delta.days


def to_iso_string(dt: datetime) -> str:
    """Convert datetime to ISO 8601 string."""
    return dt.isoformat()


def from_iso_string(iso_str: str) -> datetime:
    """Parse ISO 8601 string to datetime."""
    return datetime.fromisoformat(iso_str)






