import os
from typing import Any, Dict

class AppConfig:
    def __init__(self, env_prefix: str = 'PYU61_'):
        self._data: Dict[str, Any] = {}
        self._prefix = env_prefix
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                clean_key = key[len(self._prefix):].lower()
                self._data[clean_key] = self._cast_value(value)

    def _cast_value(self, val: str) -> Any:
        if val.lower() in ('true', 'yes'): return True
        if val.lower() in ('false', 'no'): return False
        try: return int(val)
        except ValueError:
            try: return float(val)
            except ValueError: return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key.lower(), default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key.lower()]

    def __repr__(self) -> str:
        return f'<AppConfig keys={list(self._data.keys())}>'

instance = AppConfig()