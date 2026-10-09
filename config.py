import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], prefix: str = "APP_"):
        self._defaults = defaults
        self._prefix = prefix

    def __getattr__(self, name: str) -> Any:
        env_key = f"{self._prefix}{name.upper()}"
        val = os.environ.get(env_key)

        if name not in self._defaults and val is None:
            raise AttributeError(f"Configuration parameter '{name}' is not defined")

        default_val = self._defaults.get(name)

        if isinstance(default_val, dict):
            if val:
                try:
                    return ConfigLoader(json.loads(val), prefix=f"{env_key}_")
                except json.JSONDecodeError:
                    pass
            return ConfigLoader(default_val, prefix=f"{env_key}_")

        if val is not None:
            if default_val is not None:
                try:
                    t = type(default_val)
                    if t is bool:
                        return val.lower() in ("true", "1", "yes", "on")
                    return t(val)
                except (ValueError, TypeError):
                    return val
            return val

        return default_val

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(str(err)) from err

    def get_all(self) -> Dict[str, Any]:
        result = {}
        for key, val in self._defaults.items():
            resolved = getattr(self, key)
            if isinstance(resolved, ConfigLoader):
                result[key] = resolved.get_all()
            else:
                result[key] = resolved
        return result