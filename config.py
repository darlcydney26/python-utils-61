import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self.config = defaults

    def __getitem__(self, key: str) -> Any:
        return self.config.get(key)

    def load_from_json(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        return self

    def merge_env(self, prefix: str = "APP_") -> 'ConfigLoader':
        for key in self.config:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val:
                self.config[key] = type(self.config[key])(env_val)
        return self

    def __repr__(self) -> str:
        return f"Config(values={self.config})"

def get_app_config(path: str = "config.json") -> Dict[str, Any]:
    loader = ConfigLoader({
        "host": "127.0.0.1",
        "port": 8080,
        "debug": False
    })
    return loader.load_from_json(path).merge_env().config