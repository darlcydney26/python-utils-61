import time
import random
from functools import wraps
from typing import Callable, Any, Dict, Type

def adaptive_backoff():
    """
    A generator that manages backoff delays and adapts based on feedback
    sent back into the generator via .send().
    """
    delay = 1.0
    while True:
        feedback = yield delay
        if feedback == "heavy":
            delay = min(30.0, delay * 2.5)
        elif feedback == "light":
            delay = max(0.2, delay * 1.2)
        else:
            delay = min(15.0, delay * 1.8)
        # Inject slight deterministic jitter to prevent thundering herd
        delay += random.uniform(-0.05, 0.05)
        delay = max(0.1, delay)

def retry_on_failure(retries: int = 3, severity_map: Dict[Type[Exception], str] = None):
    """
    A decorator that retries network operations utilizing an adaptive backoff
    generator to modify wait times based on the type of exception encountered.
    """
    mapping = severity_map or {}

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_flow = adaptive_backoff()
            delay = next(backoff_flow)
            
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == retries:
                        raise exc
                    
                    # Classify exception severity for the backoff adjustment
                    severity = "standard"
                    for exc_class, level in mapping.items():
                        if isinstance(exc, exc_class):
                            severity = level
                            break
                    
                    time.sleep(delay)
                    delay = backoff_flow.send(severity)
        return wrapper
    return decorator
