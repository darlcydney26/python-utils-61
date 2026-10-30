import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A whimsical configuration loader that bends reality to provide defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                user_config = json.load(f)
                self._recursive_update(self._data, user_config)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _recursive_update(self, base: dict, update: dict) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._recursive_update(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"Configuration missing: {item}")

    def __repr__(self) -> str:
        return f"ConfigLoader(keys={list(self._data.keys())})"