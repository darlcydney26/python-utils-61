import os
import json
from typing import Any, Dict, Optional

class ConfigHandler:
    def __init__(self, defaults: Optional[Dict[str, Any]] = None, config_path: Optional[str] = None):
        self._defaults = defaults or {}
        self._config: Dict[str, Any] = self._defaults.copy()
        if config_path:
            self._load_from_file(config_path)
        self._load_from_environment()

    def _load_from_file(self, path: str) -> None:
        if os.path.isfile(path):
            try:
                with open(path, 'r') as f:
                    file_config = json.load(f)
                    if isinstance(file_config, dict):
                        self._config.update(file_config)
            except (json.JSONDecodeError, IOError, OSError):
                pass

    def _load_from_environment(self) -> None:
        for key in list(self._config.keys()):
            env_var = f"CONFIG_{key.upper()}"
            if env_var in os.environ:
                value = os.environ[env_var]
                orig = self._config[key]
                if isinstance(orig, bool):
                    self._config[key] = value.lower() in ('true', '1', 'yes')
                elif isinstance(orig, int):
                    try:
                        self._config[key] = int(value)
                    except ValueError:
                        pass
                elif isinstance(orig, float):
                    try:
                        self._config[key] = float(value)
                    except ValueError:
                        pass
                else:
                    self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        if key in self._config:
            return self._config[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._config

    def as_dict(self) -> Dict[str, Any]:
        return self._config.copy()

    def __getattr__(self, name: str) -> Any:
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")