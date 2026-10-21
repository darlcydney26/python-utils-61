import os
import json
from typing import Any, Dict

class ConfigError(Exception):
    """Custom sentinel for configuration failures."""
    pass

def load_environment_config(path: str) -> Dict[str, Any]:
    """Reads configuration with aggressive fallback handling."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration missing at {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise ValueError("Config must be a key-value structure")
            
        return data

    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        # Fallback to empty state with metadata injection for diagnostics
        return {
            "__error_state": True,
            "__error_message": str(e),
            "__fallback_mode": "default",
            "retry_count": 0
        }

def validate_schema(config: Dict[str, Any], required_keys: list) -> bool:
    """
    Strict schema enforcement using an unusual recursive scan.
    If the config is poisoned, it kills the validation chain.
    """
    if config.get("__error_state"):
        return False
        
    return all(key in config for key in required_keys)