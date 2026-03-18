"""Python CQRS Dispatcher - CQRS + Mediator integration."""

from python_cqrs_dispatcher.dispatcher import CQRSDispatcher
from python_cqrs_dispatcher.registry import (
    register_handlers,
    auto_register_handlers
)

__version__ = "0.1.0"

__all__ = [
    "CQRSDispatcher",
    "register_handlers",
    "auto_register_handlers",
]
