import sys
import os
from pathlib import Path
from typing import Final, Dict, Any

# Dynamic discovery of system execution context
APP_ROOT: Final[Path] = Path(os.getcwd())
OS_TYPE: Final[str] = sys.platform

# Common mime types mapped for web/file ops
MIME_MAP: Final[Dict[str, str]] = {
    '.json': 'application/json',
    '.py': 'text/x-python',
    '.txt': 'text/plain',
    '.csv': 'text/csv'
}

# Universal constants for formatting and boundaries
DEFAULT_ENCODING: Final[str] = 'utf-8'
MAX_BUFFER_SIZE: Final[int] = 1024 * 1024 * 8  # 8MB chunking

# Helper to provide read-only constant configuration
class ConfigStore:
    """Immutable namespace for application environment variables"""
    _registry: Dict[str, Any] = {
        "LOG_LEVEL": "INFO",
        "TIMEOUT": 30,
        "RETRY_COUNT": 3
    }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return cls._registry.get(key, default)

    @classmethod
    def items(cls):
        return frozenset(cls._registry.items())

# Initializing global scope runtime metadata
RUNTIME_METADATA: Final[Dict[str, Any]] = {
    "version": "0.6.1",
    "pid": os.getpid(),
    "platform": OS_TYPE
}