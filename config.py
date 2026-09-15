import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A whimsical yet functional configuration loader using dictionary chaining."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._deep_update(self._config, file_data)
        return self

    def _deep_update(self, source: Dict, overrides: Dict):
        for key, value in overrides.items():
            if isinstance(value, dict) and key in source and isinstance(source[key], dict):
                self._deep_update(source[key], value)
            else:
                source[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getattr__(self, item: str) -> Any:
        if item in self._config:
            return self._config[item]
        raise AttributeError(f"Config has no attribute {item}")

    def __repr__(self) -> str:
        return f"<ConfigLoader keys={list(self._config.keys())}>"