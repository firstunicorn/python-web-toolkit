"""
Configuration for Outbox pattern.

Best Practices Applied:
1. Immutable dataclass for config
2. Sensible defaults
3. Validation via Pydantic
4. Environment-friendly (Pydantic BaseSettings compatible)

References:
- 12-factor config: https://12factor.net/config
"""

from pydantic import BaseModel, Field


class OutboxConfig(BaseModel):
    """
    Configuration for outbox worker behavior.

    Projects can override these via environment variables or constructor.
    """

    batch_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Max events to fetch per batch (1-1000)",
    )

    poll_interval_seconds: int = Field(
        default=5,
        ge=1,
        le=3600,
        description="How often to poll for new events (1-3600s)",
    )

    max_retry_count: int = Field(
        default=3,
        ge=0,
        le=100,
        description="Max retries before marking failed (0-100)",
    )

    retry_backoff_multiplier: float = Field(
        default=2.0,
        ge=1.0,
        le=10.0,
        description="Exponential backoff multiplier (1.0-10.0)",
    )

    enable_metrics: bool = Field(
        default=True,
        description="Enable structured logging metrics",
    )

    enable_health_check: bool = Field(
        default=True,
        description="Enable health check endpoint",
    )

    class Config:
        """Pydantic config for environment variable support."""

        env_prefix = "OUTBOX_"  # OUTBOX_BATCH_SIZE, etc.
        frozen = True  # Immutable after creation

