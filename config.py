import os
from typing import Any, Dict

class ConfigRegistry:
    """Dynamic attribute-based configuration storage."""
    def __init__(self, **entries: Any) -> None:
        self._data = entries

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name, None)

    def update_from_env(self, prefix: str = "APP_") -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value

    def dump(self) -> Dict[str, Any]:
        return {k: v for k, v in self._data.items()}

def load_defaults() -> ConfigRegistry:
    return ConfigRegistry(
        environment="development",
        debug=True,
        version="1.0.0",
        retries=3
    )

config = load_defaults()
config.update_from_env()