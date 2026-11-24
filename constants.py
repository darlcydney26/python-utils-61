import sys
import os
from pathlib import Path
from typing import Final, Any, Dict

# Dynamic discovery of system environmental parameters
APP_NAME: Final[str] = 'python-utils-61'
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Creative mapping for common path abstractions
SYSTEM_PATHS: Final[Dict[str, Path]] = {
    'log': BASE_DIR / 'logs',
    'cache': Path(os.getenv('TMPDIR', '/tmp')) / APP_NAME,
    'data': BASE_DIR / 'data'
}

# Unusual byte-to-human conversion constants using binary prefixes
STORAGE_UNITS: Final[tuple] = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB')

# Execution environment state flags
IS_DEBUG: Final[bool] = bool(os.getenv('DEBUG', False))
PLATFORM_ID: Final[str] = sys.platform

class ExitCodes:
    SUCCESS: int = 0
    GENERAL_ERROR: int = 1
    CONFIG_MISSING: int = 2
    NETWORK_TIMEOUT: int = 3

def ensure_paths() -> None:
    """Automated directory initialization for utility ops"""
    for path in SYSTEM_PATHS.values():
        path.mkdir(parents=True, exist_ok=True)

# Execute initialization on module load
if __name__ != '__main__':
    ensure_paths()