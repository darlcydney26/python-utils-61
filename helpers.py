import time
import random
import functools
from typing import Callable, Type, Tuple, Any, Generator


def backoff_stream(base_delay: float = 0.2, max_delay: float = 5.0, factor: float = 2.0) -> Generator[float, None, None]:
    """Generator producing exponential backoff intervals with randomized jitter."""
    delay = base_delay
    while True:
        jittered_wait = random.uniform(0, min(max_delay, delay))
        yield jittered_wait
        delay = min(max_delay, delay * factor)


def retry_network_op(
    retries: int = 3,
    handled_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    backoff_generator: Callable[[], Generator[float, None, None]] = backoff_stream
):
    """Decorator implementing robust retry mechanics via dynamic generator streams."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = backoff_generator()
            last_exception = None
            
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except handled_exceptions as exc:
                    last_exception = exc
                    if attempt == retries:
                        break
                    sleep_duration = next(delays)
                    time.sleep(sleep_duration)
            
            if last_exception:
                raise last_exception
        return wrapper
    return decorator


class ResilientRequestRunner:
    """Wrapper class to execute arbitrary network callables with resilience."""
    def __init__(self, retries: int = 4):
        self.retries = retries

    def run(self, operation: Callable[[], Any]) -> Any:
        @retry_network_op(retries=self.retries)
        def _dispatch():
            return operation()
        return _dispatch()
