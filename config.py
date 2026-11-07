import json
import os
from typing import Any, Dict, Optional, Union

class ConfigLoadError(Exception):
    """Base exception for config loading failures."""
    pass

class SafeConfig:
    """Dynamic configuration container with self-healing edge-case recovery."""
    
    _SENTINEL = object()

    def __init__(self, defaults: Optional[Dict[str, Any]] = None):
        self._data: Dict[str, Any] = defaults or {}
        self._fallbacks: Dict[str, Any] = {}

    def load_from_env(self, prefix: str = "APP_") -> "SafeConfig":
        """Loads env vars matching prefix with graceful type coercion."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = self._coerce_value(value)
        return self

    def load_json(self, filepath: str, ignore_corrupt: bool = True) -> "SafeConfig":
        """Loads JSON file with fallback recovery for malformed or missing data."""
        try:
            if not os.path.exists(filepath):
                raise ConfigLoadError(f"File not found: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if isinstance(content, dict):
                    self._data.update(content)
        except (json.JSONDecodeError, OSError, ConfigLoadError) as err:
            if not ignore_corrupt:
                raise
            self._fallbacks['last_error'] = str(err)
        return self

    def _coerce_value(self, raw: str) -> Union[int, float, bool, str]:
        """Tries to coerce string values into primitive Python types safely."""
        cleaned = raw.strip()
        if cleaned.lower() in ("true", "1", "yes"):
            return True
        if cleaned.lower() in ("false", "0", "no"):
            return False
        for type_func in (int, float):
            try:
                return type_func(cleaned)
            except ValueError:
                continue
        return raw

    def get(self, key: str, fallback: Any = _SENTINEL) -> Any:
        """Retrieve key with recursive fallback resolution."""
        try:
            keys = key.split('.')
            val = self._data
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            if fallback is not self._SENTINEL:
                return fallback
            return self._fallbacks.get(key, None)

    def __getattr__(self, name: str) -> Any:
        val = self.get(name, self._SENTINEL)
        if val is self._SENTINEL:
            raise AttributeError(f"Configuration key '{name}' does not exist")
        return val