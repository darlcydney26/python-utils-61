import datetime
import inspect
import sys
from typing import Any

class DataLogger:
    """An unconventional stream-based data interceptor."""
    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def __call__(self, obj: Any, label: str = "DEBUG") -> Any:
        caller = inspect.stack()[1]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = f"{caller.function}@{caller.lineno}"
        
        payload = {
            "ts": timestamp,
            "loc": context,
            "lbl": label,
            "val": repr(obj)
        }
        
        formatted = " | ".join(f"{k}={v}" for k, v in payload.items())
        self.stream.write(f"[DATA-TRAP] {formatted}\n")
        return obj

log = DataLogger()

def tap(data: Any, label: str = "LOG") -> Any:
    return log(data, label)

if __name__ == "__main__":
    # Example usage: tap(x) returns x while side-effecting to stdout
    result = tap([1, 2, 3], label="INIT_LIST")
    assert result == [1, 2, 3]