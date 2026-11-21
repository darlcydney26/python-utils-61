import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self.data = defaults.copy()
        self.env_prefix = env_prefix

    def load(self, path: str = None) -> 'ConfigLoader':
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                self.data.update(json.load(f))
        self._load_env()
        return self

    def _load_env(self):
        for key in self.data:
            env_val = os.environ.get(f"{self.env_prefix}{key.upper()}")
            if env_val is not None:
                try:
                    self.data[key] = json.loads(env_val)
                except (json.JSONDecodeError, TypeError):
                    self.data[key] = env_val

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Config has no attribute {name}")

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<ConfigLoader({list(self.data.keys())})>"