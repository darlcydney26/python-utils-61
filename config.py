import json
import os
from typing import Any, Dict, Iterator, Mapping, Optional


class ConfigNode(Mapping):
    """Hierarchical config loader with default fallback and environment resolution."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "CONFIG_") -> None:
        self._defaults = defaults or {}
        self._overrides: Dict[str, Any] = {}
        self._prefix = env_prefix

    def load_file(self, path: str) -> "ConfigNode":
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                self._overrides.update(json.load(file))
        return self

    def load_dict(self, data: Dict[str, Any]) -> "ConfigNode":
        self._overrides.update(data)
        return self

    def _resolve_env(self, key: str) -> Any:
        env_key = f"{self._prefix}{key.upper()}"
        if env_key in os.environ:
            raw = os.environ[env_key]
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                return raw
        return None

    def __getitem__(self, key: str) -> Any:
        env_val = self._resolve_env(key)
        if env_val is not None:
            val = env_val
        elif key in self._overrides:
            val = self._overrides[key]
        elif key in self._defaults:
            val = self._defaults[key]
        else:
            raise KeyError(key)

        if isinstance(val, dict):
            return ConfigNode(val, env_prefix=f"{self._prefix}{key.upper()}_")
        return val

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"Config option '{name}' not found") from None

    def __iter__(self) -> Iterator[str]:
        return iter(set(self._defaults.keys()) | set(self._overrides.keys()))

    def __len__(self) -> int:
        return len(set(self._defaults.keys()) | set(self._overrides.keys()))

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
