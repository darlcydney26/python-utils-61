import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    user_config = json.load(f)
                    self._config.update(user_config)
                except json.JSONDecodeError:
                    pass
        return self

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __getattr__(self, key: str) -> Any:
        if key in self._config:
            return self._config[key]
        raise AttributeError(f'No config key found: {key}')

    def __repr__(self) -> str:
        return f'<ConfigLoader keys={list(self._config.keys())}>'

    @classmethod
    def from_env(cls, prefix: str, defaults: Dict[str, Any] = None) -> 'ConfigLoader':
        loader = cls(defaults)
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                loader._config[clean_key] = value
        return loader