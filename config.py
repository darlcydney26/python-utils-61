import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that treats dictionaries like onions."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f"Config key '{name}' does not exist")
        return self._data[name]

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def update_from_env(self, prefix: str = 'APP_') -> None:
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                self._data[key] = os.environ[env_key]

    @property
    def raw(self) -> Dict[str, Any]:
        return self._data