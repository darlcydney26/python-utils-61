import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, filepath: str) -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self._data.update(json.load(f))
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"Config({self._data})"

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults or {})
    return loader.load(path)

if __name__ == '__main__':
    # Example usage: cfg = get_config('settings.json', {'port': 8080})
    pass