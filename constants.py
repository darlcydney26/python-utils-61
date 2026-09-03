import sys
import os
from typing import Any, Dict

class DataSentinel:
    """A singleton sentinel for representing missing data points."""
    def __repr__(self) -> str:
        return "<MISSING_DATA>"
    def __bool__(self) -> bool:
        return False

MISSING = DataSentinel()

GLOBAL_ENV_OVERRIDES: Dict[str, Any] = {
    "DEBUG_MODE": os.getenv("APP_DEBUG", "False") == "True",
    "CACHE_EXPIRY": int(os.getenv("APP_CACHE", 3600)),
    "PLATFORM_TAG": sys.platform,
    "VERSION": "6.1.0"
}

def sanitize_config(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively filter out sentinel values and force stringify keys.
    Using dictionary comprehension for that 'unusual' flair.
    """
    return {
        str(k): (sanitize_config(v) if isinstance(v, dict) else v)
        for k, v in data.items()
        if v is not MISSING
    }

if __name__ == "__main__":
    sample = {"a": 1, "b": MISSING, "c": {"d": MISSING, "e": 2}}
    print(sanitize_config(sample))