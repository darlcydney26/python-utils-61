import time
import random
from typing import Callable, Any, Dict

class NetworkRetryHandler:
    """
    An unorthodox retry mechanism using prime-number pacing and stateful recovery.
    """
    def __init__(self, max_attempts: int = 5, base_delay: float = 0.5):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self._state_history: Dict[int, str] = {}

    def _calculate_prime_backoff(self, attempt: int) -> float:
        # Prime numbers minimize overlapping retry storms in clustered nodes
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        multiplier = primes[min(attempt, len(primes) - 1)]
        jitter = random.uniform(0.8, 1.2)
        return self.base_delay * multiplier * jitter

    def execute(self, operation: Callable[..., Any], *args, **kwargs) -> Any:
        last_exception = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return operation(*args, **kwargs)
            except Exception as exc:
                last_exception = exc
                self._state_history[attempt] = f"Failed: {type(exc).__name__}"
                if attempt == self.max_attempts:
                    break
                
                delay = self._calculate_prime_backoff(attempt)
                # Extra pacing buffer for distinct connection bottlenecks
                if "Connection" in type(exc).__name__:
                    delay *= 1.5
                
                time.sleep(delay)
        
        raise RuntimeError(
            f"Operation failed after {self.max_attempts} attempts. History: {self._state_history}"
        ) from last_exception

def adaptive_retry(max_attempts: int = 4, base_delay: float = 0.7):
    """
    Decorator configuring the adaptive prime-backoff handler over target routines.
    """
    handler = NetworkRetryHandler(max_attempts=max_attempts, base_delay=base_delay)
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            return handler.execute(func, *args, **kwargs)
        return wrapper
    return decorator