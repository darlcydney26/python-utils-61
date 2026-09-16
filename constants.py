from typing import Final, Dict, Any

# Configuration constants for python-utils-61
# Using a creative approach with a dict-based access container

MAX_RETRIES: Final[int] = 5
DEFAULT_TIMEOUT: Final[float] = 30.5
ENVIRONMENT_VAR: Final[str] = "PY_UTILS_ENV"

class ConfigSchema:
    """Container for structured application constants."""
    
    SETTINGS: Final[Dict[str, Any]] = {
        "version": "1.0.0",
        "debug": False,
        "log_level": "INFO"
    }

def get_retry_delay(attempt: int) -> float:
    """
    Calculates exponential backoff for retries.
    
    :param attempt: The current retry attempt count
    :return: Calculated sleep duration in seconds
    """
    return float(2 ** attempt)

# Global flag indicating system state
SYSTEM_ACTIVE: Final[bool] = True