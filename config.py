import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_json(self, file_path: str) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                file_data = json.load(f)
                self._data.update(file_data)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Key {name} not found')

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_json(path)
    return loader

# Example usage:
# cfg = get_config('settings.json', {'debug': False, 'port': 8080})
# print(cfg.port)