from typing import Final, Any, Dict
from collections import UserDict

class DataRegistry(UserDict):
    """
    A container that acts as a read-only registry
    with dictionary-like attribute access.
    """
    def __init__(self, data: Dict[str, Any] = None):
        super().__init__(data or {})

    def __getattr__(self, item: str) -> Any:
        if item in self.data:
            return self.data[item]
        raise AttributeError(f"Registry has no key: {item}")

    def __setattr__(self, key: str, value: Any) -> None:
        if key == 'data':
            super().__setattr__(key, value)
        else:
            raise TypeError("Registry keys are immutable after initialization")

DEFAULT_CONFIG: Final = DataRegistry({
    "TIMEOUT": 30,
    "RETRY_LIMIT": 3,
    "CACHE_ENABLED": True,
    "VERSION": "1.0.0"
})

ERROR_CODES: Final[Dict[str, int]] = {
    "SUCCESS": 200,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "SERVER_ERROR": 500
}

def get_status_message(code: int) -> str:
    return {v: k for k, v in ERROR_CODES.items()}.get(code, "UNKNOWN_ERROR")