"""PipelineBehavior protocol definition."""

from typing import Any, Callable, Protocol, Optional


class PipelineBehavior(Protocol):
    """Protocol for pipeline behaviors.

    Behaviors execute before handler and can:
    - Log/monitor requests
    - Validate requests
    - Transform requests
    - Short-circuit execution

    Example:
        >>> class CustomBehavior:
        ...     async def handle(self, request, next):
        ...         # Custom logic
        ...         return await next(request)
    """

    async def handle(
        self,
        request: Any,
        next: Callable
    ) -> Optional[Any]:
        """Handle request in pipeline.

        Args:
            request: Request to handle
            next: Next handler in pipeline

        Returns:
            Result (or None to continue pipeline)
        """
        ...
