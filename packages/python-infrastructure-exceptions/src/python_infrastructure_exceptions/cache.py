"""Cache infrastructure exceptions."""

from .base import InfrastructureException


class CacheError(InfrastructureException):
    """
    Cache infrastructure error.

    Use for:
    - Redis connection failures
    - Memcached unavailable
    - Cache miss (when critical)
    - Serialization errors
    - Cache invalidation failures

    Examples:
        raise CacheError("Redis connection failed", details="Connection refused to localhost:6379")
        raise CacheError("Cache serialization failed", details="Object not pickle-able")
        raise CacheError("Cache miss for critical key", details="key=user_session_123")
    """

    def __init__(
        self,
        message: str,
        details: str = None,
        cache_backend: str = None,
        key: str = None
    ):
        """
        Initialize cache error.

        Args:
            message: Human-readable error message
            details: Optional technical details
            cache_backend: Optional cache backend name (e.g., "redis", "memcached")
            key: Optional cache key that caused the error
        """
        self.cache_backend = cache_backend
        self.key = key
        super().__init__(message, details)

