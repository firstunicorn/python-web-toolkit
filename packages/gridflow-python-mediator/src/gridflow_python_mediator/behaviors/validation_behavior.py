"""Validation pipeline behavior for Pydantic models."""

from typing import Any, Callable, Optional


class ValidationBehavior:
    """Pipeline behavior for request validation.

    Validates Pydantic models before handler execution.

    Example:
        >>> mediator.add_pipeline_behavior(
        ...     ValidationBehavior().handle
        ... )
    """

    async def handle(
        self,
        request: Any,
        next: Callable
    ) -> Optional[Any]:
        """Validate request.

        Args:
            request: Request to validate
            next: Next handler

        Returns:
            Handler result

        Raises:
            ValidationError: If validation fails
        """
        # Validate if Pydantic model
        if hasattr(request, 'model_validate'):
            request.model_validate(request)

        return await next(request)
