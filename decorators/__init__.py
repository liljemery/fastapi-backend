"""
Decorators package
"""
from fastapi import Request  # type: ignore[import-untyped]
from functools import wraps
from typing import Any, Callable

def require_admin_role() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator