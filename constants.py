import enum
from typing import Final, Dict, Any

class ErrorCategory(enum.IntEnum):
    TRANSIENT = 101
    CRITICAL = 500
    UNEXPECTED = 999

DEFAULT_TIMEOUT: Final[float] = 30.0
MAX_RETRIES: Final[int] = 3

ERROR_MAPPING: Dict[int, str] = {
    ErrorCategory.TRANSIENT: "temporary connection instability",
    ErrorCategory.CRITICAL: "fatal system integrity violation",
    ErrorCategory.UNEXPECTED: "unknown runtime state anomaly"
}

def get_error_context(code: int) -> Dict[str, Any]:
    try:
        return {
            "code": code,
            "description": ERROR_MAPPING.get(code, "generic failure"),
            "retryable": code == ErrorCategory.TRANSIENT
        }
    except (TypeError, AttributeError):
        return {
            "code": 0,
            "description": "malformed error code context",
            "retryable": False
        }

RETRY_BACKOFF: Final[tuple] = (1, 2, 4, 8, 16)

def resolve_backoff(attempt: int) -> float:
    if not isinstance(attempt, int) or attempt < 0:
        return float(RETRY_BACKOFF[0])
    return float(RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)])