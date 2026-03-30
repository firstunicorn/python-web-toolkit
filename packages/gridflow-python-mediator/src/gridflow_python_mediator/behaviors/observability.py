"""Logging and timing pipeline behaviors."""

from typing import Any, Callable, Optional
import time

try:
    import structlog
    logger = structlog.get_logger()
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class LoggingBehavior:
    """Pipeline behavior for logging requests.

    Logs request type before and after handler execution.

    Example:
        >>> mediator.add_pipeline_behavior(
        ...     LoggingBehavior().handle
        ... )
    """

    async def handle(
        self,
        request: Any,
        next: Callable
    ) -> Optional[Any]:
        """Log request handling.

        Args:
            request: Request being handled
            next: Next handler

        Returns:
            None (continues to handler)
        """
        request_type = type(request).__name__
        logger.info("Handling request", request_type=request_type)

        result = await next(request)

        logger.info("Request completed", request_type=request_type)
        return result


class TimingBehavior:
    """Pipeline behavior for timing request execution.

    Measures and logs execution duration.

    Example:
        >>> mediator.add_pipeline_behavior(
        ...     TimingBehavior().handle
        ... )
    """

    async def handle(
        self,
        request: Any,
        next: Callable
    ) -> Optional[Any]:
        """Time request handling.

        Args:
            request: Request being handled
            next: Next handler

        Returns:
            Handler result
        """
        start = time.time()
        request_type = type(request).__name__

        result = await next(request)

        duration_ms = int((time.time() - start) * 1000)
        logger.info(
            "Request timing",
            request_type=request_type,
            duration_ms=duration_ms
        )

        return result
