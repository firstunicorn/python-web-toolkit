"""Database-specific infrastructure exceptions."""

from .base import InfrastructureException


class DatabaseError(InfrastructureException):
    """
    Database infrastructure error.

    Use for:
    - Connection pool exhaustion
    - Query timeouts
    - Transaction failures
    - Migration errors
    - Connection refused

    Examples:
        raise DatabaseError("Connection pool exhausted", details="Max connections: 20")
        raise DatabaseError("Query timeout", details="SELECT took > 30s")
        raise DatabaseError("Transaction rollback failed")
    """

    def __init__(self, message: str, details: str = None, query: str = None):
        """
        Initialize database error.

        Args:
            message: Human-readable error message
            details: Optional technical details
            query: Optional SQL query that failed (sanitized)
        """
        self.query = query
        super().__init__(message, details)

