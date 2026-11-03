import functools
import random
import time
from typing import Any, Callable, Generator, TypeVar

T = TypeVar("T")

def _backoff_stream(
    base_delay: float, max_delay: float, factor: float, jitter: bool
) -> Generator[float, None, None]:
    delay = base_delay
    while True:
        current = min(delay, max_delay)
        if jitter:
            current = random.uniform(0.5 * current, 1.5 * current)
        yield current
        delay *= factor

class NetworkRetryHandler:
    def __init__(
        self,
        max_attempts: int = 5,
        base_delay: float = 0.5,
        max_delay: float = 10.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: tuple[type[BaseException], ...] = (Exception,),
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delays = _backoff_stream(
                self.base_delay, self.max_delay, self.backoff_factor, self.jitter
            )
            attempts = 0
            while True:
                try:
                    attempts += 1
                    return func(*args, **kwargs)
                except self.retryable_exceptions as err:
                    if attempts >= self.max_attempts:
                        raise err
                    wait_seconds = next(delays)
                    time.sleep(wait_seconds)

        return wrapper

def retry_operation(
    func: Callable[..., T],
    retries: int = 3,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[..., T]:
    handler = NetworkRetryHandler(max_attempts=retries, retryable_exceptions=exceptions)
    return handler(func)
