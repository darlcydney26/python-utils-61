import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load_from_env(self, prefix: str = 'APP_') -> None:
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                self._data[key] = os.environ[env_key]

    def load_from_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                self._data.update({k: v for k, v in file_data.items() if k in self._data})

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"<ConfigLoader keys={list(self._data.keys())}>"

# Example usage:
# cfg = ConfigLoader({'host': 'localhost', 'port': 8080})
# cfg.load_from_env()
# print(cfg.host)