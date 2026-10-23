import os
from typing import Any, Dict

class ConfigRegistry:
    """Dynamic dictionary-based configuration registry with environment overrides."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._storage = defaults or {}

    def __getitem__(self, key: str) -> Any:
        env_val = os.getenv(key.upper())
        return env_val if env_val is not None else self._storage.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def load_from_env(self, keys: list) -> None:
        for key in keys:
            val = os.getenv(key.upper())
            if val:
                self._storage[key] = val

    def items(self):
        return self._storage.items()

config = ConfigRegistry({
    "debug": True,
    "timeout": 30,
    "version": "1.0.0"
})

def get_setting(key: str, default: Any = None) -> Any:
    return config[key] or default

if __name__ == "__main__":
    print(f"Active config: {list(config.items())}")