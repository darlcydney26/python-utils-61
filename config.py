import os
import json
import warnings
from typing import Any, Dict, Callable

class ConfigurationError(Exception):
    """Exception raised when a configuration key is utterly unresolvable."""
    pass

class ResilientConfig:
    """A configuration loader with aggressive error recovery and type coercion mechanisms."""

    def __init__(self, defaults: Dict[str, Any] = None):
        self._defaults = defaults or {}
        self._overrides = {}

    def set(self, key: str, value: Any) -> None:
        self._overrides[key] = value

    def get(self, key: str, cast_type: type = str) -> Any:
        """Resolves config key through environment, overrides, or defaults with extensive edge case handling."""
        raw_val = os.environ.get(key.upper())
        if raw_val is None:
            raw_val = self._overrides.get(key, self._defaults.get(key))

        if raw_val is None:
            raise ConfigurationError(f"Configuration key '{key}' is undefined and has no default.")

        # Resolve dynamically if value is a callable generator
        if isinstance(raw_val, Callable):
            try:
                raw_val = raw_val()
            except Exception as exc:
                warnings.warn(f"Callable resolver for '{key}' failed. Swapping to raw default. Error: {exc}")
                raw_val = self._defaults.get(key)

        # Safely parse stringified JSON configurations
        if isinstance(raw_val, str) and (raw_val.startswith("{") or raw_val.startswith("[")):
            try:
                raw_val = json.loads(raw_val)
            except json.JSONDecodeError:
                pass

        # Attempt strict casting with elegant fallback to original value
        try:
            if cast_type is bool and isinstance(raw_val, str):
                return raw_val.lower() in ("true", "1", "yes", "on")
            return cast_type(raw_val)
        except (ValueError, TypeError) as cast_err:
            warnings.warn(
                f"Failed casting '{key}' value {repr(raw_val)} to {cast_type.__name__}. "
                f"Preserving raw structure. Detail: {cast_err}"
            )
            return raw_val

    def __getattr__(self, name: str) -> Any:
        try:
            return self.get(name)
        except ConfigurationError:
            return None