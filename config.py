import os
import json
from collections import ChainMap
from typing import Any, Dict, Optional


class ConfigLoader:
    """Dynamic configuration loader with env overrides and cascading defaults."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "APP_"):
        self._defaults = defaults or {}
        self._env_prefix = env_prefix
        self._overrides: Dict[str, Any] = {}
        self._refresh()

    def _refresh(self) -> None:
        env_data = {}
        for key, default_val in self._defaults.items():
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                target_type = type(default_val) if default_val is not None else str
                try:
                    if target_type is bool:
                        env_data[key] = raw_val.lower() in ("1", "true", "yes", "on")
                    else:
                        env_data[key] = target_type(raw_val)
                except (ValueError, TypeError):
                    env_data[key] = raw_val

        self._chain = ChainMap(self._overrides, env_data, self._defaults)

    def load_dict(self, data: Dict[str, Any]) -> "ConfigLoader":
        self._overrides.update(data)
        self._refresh()
        return self

    def load_json(self, filepath: str) -> "ConfigLoader":
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self.load_dict(json.load(f))
        return self

    def __getitem__(self, key: str) -> Any:
        return self._chain[key]

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"No attribute {name}")
        try:
            return self._chain[name]
        except KeyError:
            raise AttributeError(f"Configuration key '{name}' not found") from None

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._chain.get(key, fallback)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._chain)
