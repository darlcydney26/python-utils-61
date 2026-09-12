from typing import Any, Dict, Optional, Union
import os

class AppConfig:
    """Dynamic configuration loader for python-utils-61."""
    
    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        self._data: Dict[str, Any] = settings or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve configuration value with fallback mechanism."""
        return self._data.get(key, os.getenv(key.upper(), default))

    def set(self, key: str, value: Any) -> None:
        """Update configuration dictionary runtime state."""
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        """Dictionary-like access support for settings."""
        if key not in self._data:
            raise KeyError(f"Missing required configuration key: {key}")
        return self._data[key]

    @classmethod
    def from_env(cls, prefix: str = "APP_") -> 'AppConfig':
        """Load variables from OS environment with prefix."""
        items = {k[len(prefix):]: v for k, v in os.environ.items() if k.startswith(prefix)}
        return cls(settings=items)

    def __repr__(self) -> str:
        """String representation for debugging visibility."""
        return f"AppConfig(keys={list(self._data.keys())})"