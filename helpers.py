import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A whimsical configuration loader using attribute-based access."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_json(self, file_path: str) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self._data.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config key '{name}' not found")

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def update_env(self, prefix: str = "APP_") -> None:
        """Overrides config values with environment variables."""
        for key in self._data:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val:
                self._data[key] = env_val

def create_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults or {})

# Usage example:
# cfg = create_config({'host': 'localhost', 'port': 8080})
# cfg.load_from_json('settings.json')
# cfg.update_env()
# print(f"Running on {cfg.host}:{cfg.port}")