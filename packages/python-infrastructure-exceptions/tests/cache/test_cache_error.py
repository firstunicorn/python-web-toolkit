"""Unit tests for CacheError.

Tests cache-related infrastructure exceptions.
RULE: Maximum 100 lines per file.
"""

import pytest

from python_infrastructure_exceptions import CacheError


class TestCacheError:
    """Tests for CacheError."""

    def test_cache_error_basic(self):
        """CacheError should accept message."""
        exc = CacheError("Redis connection failed")
        assert "Redis connection failed" in str(exc)

    def test_cache_error_with_cache_backend(self):
        """CacheError should accept cache_backend."""
        exc = CacheError("Connection failed", cache_backend="redis")
        assert exc.cache_backend == "redis"

    def test_cache_error_with_key(self):
        """CacheError should accept key parameter."""
        exc = CacheError("Cache miss", key="user_session_123")
        assert exc.key == "user_session_123"
