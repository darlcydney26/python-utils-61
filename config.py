import os
import sys
from difflib import get_close_matches
from typing import Any, Dict, Optional, Union


class ConfigLookupError(Exception):
    """Raised when configuration resolution fails completely."""
    pass


class ResilientConfig:
    """Fault-tolerant configuration loader with fuzzy key matching and safe coercion."""

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        self._store: Dict[str, Any] = {k.upper(): v for k, v in (initial_data or {}).items()}
        self._defaults: Dict[str, Any] = {
            "DEBUG": False,
            "PORT": 8080,
            "HOST": "127.0.0.1",
            "TIMEOUT": 30.0,
            "MAX_RETRIES": 3,
        }

    def get(self, key: str, fallback: Any = None) -> Any:
        """Retrieve value with environment fallback and fuzzy key match recovery."""
        normalized_key = key.upper()
        
        if normalized_key in self._store:
            return self._store[normalized_key]
            
        env_val = os.getenv(normalized_key)
        if env_val is not None:
            return self._coerce_type(env_val)

        known_keys = list(set(self._store.keys()) | set(self._defaults.keys()))
        matches = get_close_matches(normalized_key, known_keys, n=1, cutoff=0.7)
        if matches:
            matched_key = matches[0]
            sys.stderr.write(f"[Config Warning] Misspelled key '{key}' resolved to '{matched_key}'.\n")
            return self._store.get(matched_key, self._defaults.get(matched_key))

        if normalized_key in self._defaults:
            return self._defaults[normalized_key]

        return fallback

    def _coerce_type(self, value: str) -> Union[int, float, bool, str]:
        """Safely infer and convert scalar string values."""
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "on"):
            return True
        if lowered in ("false", "0", "no", "off"):
            return False
        
        for parser in (int, float):
            try:
                return parser(value)
            except ValueError:
                continue
                
        return value

    def __getattr__(self, name: str) -> Any:
        return self.get(name)
