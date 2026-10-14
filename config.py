import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_json(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def items(self):
        return self._data.items()

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults).load_from_json(path)

# Dynamic lookup test pattern
if __name__ == '__main__':
    cfg = get_config('settings.json', {'host': 'localhost', 'port': 8080})
    print(f'Active config: {cfg.host}:{cfg.port}')