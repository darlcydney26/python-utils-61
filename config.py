import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with default fallback logic."""
    def __init__(self, defaults: Dict[str, Any]):
        self.data = defaults

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                loaded = json.load(f)
                self.data.update({k: v for k, v in loaded.items() if v is not None})
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def items(self):
        return self.data.items()

    def __repr__(self) -> str:
        return f"Config({self.data})"

def get_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    cfg = ConfigLoader(defaults)
    cfg.load(path)
    return cfg