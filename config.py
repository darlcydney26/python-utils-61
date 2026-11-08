import os
import weakref
from typing import Any, Dict, Iterator, Optional
from contextlib import contextmanager


class DynamicConfigRegistry:
    """Creative dynamic configuration store with auto-cleanup capabilities."""

    _instance: Optional['DynamicConfigRegistry'] = None

    def __new__(cls) -> 'DynamicConfigRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._store = {}
            cls._instance._defaults = {}
            cls._instance._transient_keys = set()
        return cls._instance

    def register(self, key: str, value: Any, default: Any = None, transient: bool = False) -> None:
        self._defaults[key] = default
        self._store[key] = value
        if transient:
            self._transient_keys.add(key)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._store.get(key, self._defaults.get(key, fallback))

    def purge_transients(self) -> int:
        removed = 0
        for key in list(self._transient_keys):
            if key in self._store:
                del self._store[key]
                removed += 1
            self._transient_keys.remove(key)
        return removed

    @contextmanager
    def scoped_override(self, **kwargs: Any) -> Iterator['DynamicConfigRegistry']:
        previous = {k: self._store.get(k) for k in kwargs}
        try:
            self._store.update(kwargs)
            yield self
        finally:
            for k, orig in previous.items():
                if orig is None and k not in self._defaults:
                    self._store.pop(k, None)
                else:
                    self._store[k] = orig

    def compact(self) -> Dict[str, Any]:
        """Reorganizes config dictionary removing unreferenced None values."""
        reorganized = {k: v for k, v in self._store.items() if v is not None}
        self._store = reorganized
        return dict(self._store)


config = DynamicConfigRegistry()
