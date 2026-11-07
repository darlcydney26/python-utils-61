import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                self._data.update(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    @property
    def raw(self) -> Dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

def get_config(path: str, defaults: Dict = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load(path)
    return loader