import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> 'ConfigLoader':
        file = Path(path)
        if file.exists():
            with open(file, 'r') as f:
                loaded = json.load(f)
                self._deep_update(self._data, loaded)
        return self

    def _deep_update(self, source: Dict, overrides: Dict) -> None:
        for key, value in overrides.items():
            if isinstance(value, dict) and key in source and isinstance(source[key], dict):
                self._deep_update(source[key], value)
            else:
                source[key] = value

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self._data.keys())}>"

    @property
    def raw(self) -> Dict[str, Any]:
        return self._data

# Usage:
# cfg = ConfigLoader({"host": "localhost", "port": 8080}).load("settings.json")
# print(cfg.host)