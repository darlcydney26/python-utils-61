import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy for configuration management."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_env(self, prefix: str = "APP_") -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = self._try_parse(value)

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def _try_parse(self, val: str) -> Any:
        try:
            return json.loads(val.lower())
        except (json.JSONDecodeError, TypeError):
            return val

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

    def keys(self):
        return self._data.keys()

    def __repr__(self):
        return f"ConfigLoader({self._data})"