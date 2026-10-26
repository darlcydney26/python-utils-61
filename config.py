import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'config key {name} missing')

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def settings(self) -> Dict[str, Any]:
        return self._data

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults or {}).load(path)

if __name__ == '__main__':
    cfg = get_config('settings.json', {'host': 'localhost', 'port': 8080})
    print(f'current endpoint: {cfg.host}:{cfg.port}')