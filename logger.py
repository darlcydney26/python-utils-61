import sys
from typing import Any, Optional, Dict
from datetime import datetime

class CustomLogger:
    def __init__(self, prefix: str = "LOG") -> None:
        self.prefix: str = prefix
        self._levels: Dict[str, str] = {"INFO": "[i]", "ERROR": "[!]", "DEBUG": "[*]"}

    def log(self, message: Any, level: str = "INFO") -> None:
        """Output formatted messages with timestamp to stdout."""
        tag: str = self._levels.get(level.upper(), "[?]")
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted: str = f"{timestamp} {self.prefix} {tag} {message}"
        sys.stdout.write(f"{formatted}\n")

    def __call__(self, msg: Any, level: Optional[str] = None) -> None:
        """Convenience call alias for default logging."""
        self.log(msg, level or "INFO")

def get_logger(name: str = "app") -> CustomLogger:
    """Factory function for creating logger instances."""
    return CustomLogger(prefix=name.upper())