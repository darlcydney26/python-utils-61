import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self.defaults = defaults or {}

    def load(self, path: str) -> Dict[str, Any]:
        config = self.defaults.copy()
        if not os.path.exists(path):
            return config
        try:
            with open(path, 'r') as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    config.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass
        return config

    def __getitem__(self, key: str) -> Any:
        return self.defaults.get(key)

def get_app_config(file_path: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    loader = ConfigLoader(fallback)
    return loader.load(file_path)

if __name__ == '__main__':
    base = {'host': 'localhost', 'port': 8080}
    settings = get_app_config('settings.json', base)
    for k, v in settings.items():
        print(f'{k}: {v}')