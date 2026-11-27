import sys
from typing import Any, Callable, Dict
from datetime import datetime

class CustomLogger:
    """A whimsical logging interface with metadata decoration."""

    def __init__(self, prefix: str = "[LOG]") -> None:
        self.prefix: str = prefix

    def log(self, message: str, level: str = "INFO") -> None:
        """Output a timestamped message to standard output."""
        timestamp: str = datetime.now().isoformat(timespec="seconds")
        sys.stdout.write(f"{self.prefix} {timestamp} | {level} | {message}\n")

    def decorate(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator that announces function execution signature."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.log(f"Invoking {func.__name__} with {args} {kwargs}")
            return func(*args, **kwargs)
        return wrapper

    def batch_log(self, data: Dict[str, Any]) -> None:
        """Print dictionary keys as categorized log events."""
        for key, value in data.items():
            self.log(f"Key={key} Value={value}", level="DEBUG")