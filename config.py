import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def load(self, filepath: str) -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def env_override(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value
        return self

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

# Usage: cfg = ConfigLoader({'host': 'localhost'}).load('config.json').env_override()