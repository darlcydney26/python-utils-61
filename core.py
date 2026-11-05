import random
import time
from functools import wraps
from typing import Any, Callable, Iterable, Optional, Tuple, Type


class NetworkRetryError(Exception):
    """Raised when all retry attempts fail."""

    def __init__(self, last_exception: Exception, attempts: int):
        self.last_exception = last_exception
        self.attempts = attempts
        super().__init__(
            f"Operation failed after {attempts} attempts. Last error: {last_exception}"
        )


def fibonacci_backoff(base: float = 0.5, max_delay: float = 30.0) -> Iterable[float]:
    """Yields fibonacci backoff intervals with randomized jitter."""
    a, b = base, base
    while True:
        jitter = random.uniform(0.8, 1.2)
        yield min(a * jitter, max_delay)
        a, b = b, a + b


def resilient_call(
    retry_on: Tuple[Type[Exception], ...] = (Exception,),
    max_attempts: int = 5,
    backoff_gen: Optional[Callable[[], Iterable[float]]] = None,
) -> Callable:
    """Decorator applying dynamic backoff retry schedules to network-bound functions."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = (backoff_gen or fibonacci_backoff)()
            delay_iter = iter(delays)
            last_err = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    time.sleep(next(delay_iter))

            raise NetworkRetryError(last_err, max_attempts)

        return wrapper

    return decorator
