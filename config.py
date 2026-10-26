import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that defies boredom."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                self._data.update({k: v for k, v in file_data.items() if v is not None})

    def __repr__(self) -> str:
        return f"<ConfigLoader keys={list(self._data.keys())}>"

def get_config(defaults: Dict[str, Any], path: str = 'config.json') -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_json(path)
    return loader