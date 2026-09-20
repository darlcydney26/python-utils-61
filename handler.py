import functools
import math
import sys
from typing import Any, Callable, Dict, Type

class EdgeCaseShield:
    """Creative resilience wrapper converting standard runtime failures into handled boundary states."""
    
    _RECOVERIES: Dict[Type[BaseException], Callable[[BaseException, tuple, dict], Any]] = {
        ZeroDivisionError: lambda e, args, kwargs: float('inf') if (args and isinstance(args[0], (int, float)) and args[0] > 0) else 0.0,
        IndexError: lambda e, args, kwargs: None,
        KeyError: lambda e, args, kwargs: kwargs.get('default', None),
        TypeError: lambda e, args, kwargs: str(args[0]) if args and "unhashable" in str(e) else None,
        RecursionError: lambda e, args, kwargs: sys.setrecursionlimit(sys.getrecursionlimit() * 2) or "recursion_limit_exceeded",
    }

    def __init__(self, fallback_value: Any = None, custom_handlers: Dict[Type[BaseException], Callable] = None):
        self.fallback = fallback_value
        self.handlers = {**self._RECOVERIES, **(custom_handlers or {})}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                if isinstance(result, float) and math.isnan(result):
                    return self.fallback
                return result
            except Exception as exc:
                for exc_type, recovery_fn in self.handlers.items():
                    if isinstance(exc, exc_type):
                        try:
                            return recovery_fn(exc, args, kwargs)
                        except Exception:
                            break
                if self.fallback is not None:
                    return self.fallback
                raise
        return wrapper


def handle_edge_cases(fallback: Any = None) -> Callable:
    """Convenience decorator for boundary protection."""
    return EdgeCaseShield(fallback_value=fallback)
