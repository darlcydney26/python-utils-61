import os
import json
from typing import Any, Dict

class Config:
    """Dynamic configuration loader supporting dict cascading and env variable overrides."""
    def __init__(self, data: Dict[str, Any] = None, env_prefix: str = "APP_"):
        self._data = data or {}
        self._env_prefix = env_prefix

    def __getattr__(self, name: str) -> Any:
        env_var = f"{self._env_prefix}{name.upper()}"
        if env_var in os.environ:
            try:
                return json.loads(os.environ[env_var])
            except ValueError:
                return os.environ[env_var]

        if name not in self._data:
            prefix_to_check = f"{env_var}_"
            if any(k.startswith(prefix_to_check) for k in os.environ):
                return Config({}, env_prefix=prefix_to_check)
            raise AttributeError(f"Configuration key '{name}' is not defined")

        val = self._data[name]
        if isinstance(val, dict):
            return Config(val, env_prefix=f"{env_var}_")
        return val

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.__getattr__(key)
        except AttributeError:
            return default

    def __or__(self, fallback: 'Config') -> 'Config':
        if not isinstance(fallback, Config):
            raise TypeError("Can only merge with another Config instance")
        merged = self._deep_merge(fallback._data, self._data)
        return Config(merged, self._env_prefix)

    def _deep_merge(self, base: dict, overrides: dict) -> dict:
        res = base.copy()
        for k, v in overrides.items():
            if k in res and isinstance(res[k], dict) and isinstance(v, dict):
                res[k] = self._deep_merge(res[k], v)
            else:
                res[k] = v
        return res