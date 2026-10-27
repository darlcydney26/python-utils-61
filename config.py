import json
import os
from typing import Any, Dict


class ConfigProxy:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data: Dict[str, Any] = {}
        self._env_prefix = env_prefix
        self._flatten_and_bind(defaults)

    def _flatten_and_bind(self, source: Dict[str, Any], prefix: str = "") -> None:
        for key, val in source.items():
            full_key = f"{prefix}{key}".upper()
            if isinstance(val, dict):
                self._flatten_and_bind(val, f"{full_key}_")
            else:
                env_var = f"{self._env_prefix}{full_key}"
                raw_env = os.environ.get(env_var)
                if raw_env is not None:
                    try:
                        val = json.loads(raw_env)
                    except (json.JSONDecodeError, TypeError):
                        val = raw_env
                self._data[full_key] = val

    def load_json(self, path: str) -> "ConfigProxy":
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                self._flatten_and_bind(file_data)
        return self

    def get(self, key_path: str, fallback: Any = None) -> Any:
        normalized = key_path.replace(".", "_").upper()
        return self._data.get(normalized, fallback)

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            raise AttributeError(item)
        val = self.get(item)
        if val is not None:
            return val
        prefix = f"{item.upper()}_"
        nested = {k[len(prefix) :]: v for k, v in self._data.items() if k.startswith(prefix)}
        if nested:
            proxy = ConfigProxy({}, self._env_prefix)
            proxy._data = nested
            return proxy
        raise AttributeError(f"Configuration key '{item}' not found")