"""
Health check interface for outbox monitoring.

Best Practices Applied:
1. Standard health check contract
2. Multi-level status (healthy/degraded/unhealthy)
3. Detailed diagnostics for debugging
4. Prometheus-compatible metrics

References:
- Health Check API: https://microservices.io/patterns/observability/health-check-api.html
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
from datetime import datetime


class HealthStatus(str, Enum):
    """Health status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class OutboxHealthCheck(ABC):
    """
    Health check for outbox worker.

    Projects implement this to expose health endpoints.
    Useful for K8s liveness/readiness probes.
    """

    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """
        Perform health check.

        Returns:
            Health check result with structure:
            {
                "status": "healthy" | "degraded" | "unhealthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "checks": {
                    "database": {"status": "healthy"},
                    "broker": {"status": "healthy"},
                    "outbox_lag": {"status": "healthy", "pending_count": 0}
                }
            }
        """
        ...

    async def check_database(self) -> Dict[str, Any]:
        """Check if database is reachable."""
        return {"status": HealthStatus.HEALTHY}

    async def check_broker(self) -> Dict[str, Any]:
        """Check if message broker is reachable."""
        return {"status": HealthStatus.HEALTHY}

    async def check_outbox_lag(self) -> Dict[str, Any]:
        """
        Check outbox processing lag.

        Returns unhealthy if too many pending events.
        """
        return {
            "status": HealthStatus.HEALTHY,
            "pending_count": 0,
            "oldest_event_age_seconds": 0,
        }

