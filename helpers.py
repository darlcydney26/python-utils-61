import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, default_path: str = "config.json"):
        self.path = default_path
        self._defaults = {"debug": False, "port": 8080, "host": "127.0.0.1"}

    def load(self, override: Dict[str, Any] = None) -> Dict[str, Any]:
        data = self._defaults.copy()
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    file_data = json.load(f)
                    data.update(file_data)
            except (json.JSONDecodeError, IOError):
                pass
        if override:
            data.update(override)
        return data

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

class EnvConfig(ConfigLoader):
    def load(self, override: Dict[str, Any] = None) -> Dict[str, Any]:
        cfg = super().load(override)
        for key in cfg:
            env_val = os.getenv(f"APP_{key.upper()}")
            if env_val:
                cfg[key] = type(cfg[key])(env_val)
        return cfg