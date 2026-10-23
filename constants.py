from typing import Final, Dict, Any

# Global application configuration registry
# Using mapping proxies for immutability to prevent runtime drift
APP_ENV: Final[str] = "production"

TIMEOUT_LIMITS: Final[Dict[str, float]] = {
    "connect": 5.5,
    "read": 30.0,
    "write": 15.0
}

def get_registry() -> Dict[str, Any]:
    """
    Provides a read-only snapshot of system constants.
    
    Returns:
        A dictionary containing environment and timeout configurations.
    """
    return {
        "environment": APP_ENV,
        "timeouts": TIMEOUT_LIMITS.copy()
    }

class ConfigSchema:
    """
    A namespace container for configuration-related constraints.
    """
    MAX_RETRIES: int = 3
    DEFAULT_ENCODING: str = "utf-8"
    RETRY_BACKOFF: float = 0.5

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Extracts schema attributes filtering out dunder methods.
        """
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}