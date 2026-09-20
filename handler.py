import functools
import math
import sys
import types
from typing import Any, Callable, Union


class EdgeCaseShield:
    """A resilient wrapper catching arithmetic, recursion, and structural anomalies."""

    def __init__(self, fallback_value: Any = None, max_depth: int = 100):
        self.fallback = fallback_value
        self.max_depth = max_depth

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def protected_wrapper(*args: Any, **kwargs: Any) -> Any:
            depth = sum(
                1
                for frame in sys._current_frames().values()
                if frame.f_code == func.__code__
            )
            if depth > self.max_depth:
                return self.fallback

            sanitized_args = tuple(
                0.0 if isinstance(a, float) and (math.isnan(a) or math.isinf(a)) else a
                for a in args
            )

            try:
                result = func(*sanitized_args, **kwargs)
                if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
                    return self.fallback
                if isinstance(result, types.GeneratorType):
                    return self._wrap_generator(result)
                return result
            except (ZeroDivisionError, OverflowError, TypeError, ValueError, RecursionError):
                return self.fallback

        return protected_wrapper

    def _wrap_generator(self, gen: types.GeneratorType):
        while True:
            try:
                yield next(gen)
            except StopIteration:
                break
            except Exception:
                yield self.fallback
                break


def isolate_edge_cases(func: Callable = None, *, fallback: Any = None) -> Any:
    shield = EdgeCaseShield(fallback_value=fallback)
    return shield if func is None else shield(func)
