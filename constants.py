from typing import Final, Dict, Any, Union

# Dynamic registry of system-wide configurations
# Using a mapping proxy effect via explicit typing

TIMEOUT: Final[float] = 30.5
MAX_RETRIES: Final[int] = 5

APP_STATUS_CODES: Final[Dict[str, int]] = {
    "SUCCESS": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "SERVER_ERROR": 500
}

RETRY_STRATEGIES: Final[Dict[str, Union[int, float]]] = {
    "exponential_backoff": 2.0,
    "linear_jitter": 0.1
}

def get_constant(key: str, default: Any = None) -> Any:
    """
    Retrieves a constant value from the local namespace pool.
    
    Args:
        key: The lookup string for the requested constant.
        default: Return value if key is not found.
        
    Returns:
        The value associated with the constant or default.
    """
    source: Dict[str, Any] = {**APP_STATUS_CODES, **RETRY_STRATEGIES}
    return source.get(key, default)

# Final environment lock
VERSION: Final[str] = "0.6.1-stable"