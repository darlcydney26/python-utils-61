import os
from typing import Any, Dict

class ConfigRegistry:
    def __init__(self, prefix: str = 'APP_'):
        self._storage: Dict[str, Any] = {}
        self._prefix = prefix
        self._bootstrap()

    def _bootstrap(self) -> None:
        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                clean_key = key[len(self._prefix):].lower()
                self._storage[clean_key] = self._type_infer(value)

    @staticmethod
    def _type_infer(val: str) -> Any:
        if val.lower() in ('true', 'yes'): return True
        if val.lower() in ('false', 'no'): return False
        try:
            return int(val) if '.' not in val else float(val)
        except ValueError:
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._storage.get(key.lower(), default)

    def __getitem__(self, key: str) -> Any:
        return self._storage[key.lower()]

def load_app_config() -> ConfigRegistry:
    return ConfigRegistry()

config = load_app_config()