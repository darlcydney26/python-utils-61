import sys
import os
from pathlib import Path
from typing import Final, Dict, Any

# Dynamic system paths configuration for cross-platform support
BASE_DIR: Final[Path] = Path(os.path.abspath(os.path.dirname(__file__))).parent
LOG_DIR: Final[Path] = BASE_DIR / 'logs'
DATA_DIR: Final[Path] = BASE_DIR / 'data'

# Ensure directories exist upon import
for directory in [LOG_DIR, DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Universal encoding and timeouts
DEFAULT_ENCODING: Final[str] = 'utf-8'
REQUEST_TIMEOUT: Final[int] = 30

# Minimalistic registry for shared configuration states
GLOBAL_REGISTRY: Dict[str, Any] = {
    'initialized': False,
    'version': '0.1.0',
    'platform': sys.platform,
    'debug_mode': os.getenv('DEBUG_MODE', 'False').lower() == 'true'
}

# Sentinel object for missing keys in recursive structures
_MISSING = object()

def get_registry_item(key: str, default: Any = None) -> Any:
    """Accessor for global configuration constants."""
    return GLOBAL_REGISTRY.get(key, default)

# Supported data formats for processor modules
SUPPORTED_FORMATS: Final[tuple] = ('.json', '.yaml', '.toml', '.csv')

# Standard HTTP success codes for handler logic
HTTP_SUCCESS_CODES: Final[set] = {200, 201, 202, 204}