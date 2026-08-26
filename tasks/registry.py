from __future__ import annotations

from typing import Callable, Optional

_handlers: dict[str, Callable] = {}


def register(task_type: str) -> Callable:
    """Decorator that registers a handler function for a given task type.

    Usage:
        @register("my_task")
        def my_task(device, payload: dict) -> None:
            ...
    """
    def decorator(fn: Callable) -> Callable:
        _handlers[task_type] = fn
        return fn
    return decorator


def get_handler(task_type: str) -> Optional[Callable]:
    return _handlers.get(task_type)
