import re
import os
from pathlib import Path
from typing import Final, Pattern, Any

# Universal regex patterns for common string operations
EMAIL_PATTERN: Final[Pattern] = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
ISO_DATE_PATTERN: Final[Pattern] = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

# Dynamic environment path management
BASE_DIR: Final[Path] = Path(__file__).resolve().parent
LOG_DIR: Final[Path] = BASE_DIR / "logs"

# Application default settings and state thresholds
MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 30.5
BUFFER_SIZE: Final[int] = 1024 * 64

# Type-specific status mapping for internal state machines
STATUS_CODES: Final[dict[str, int]] = {
    "PENDING": 0,
    "PROCESSING": 1,
    "COMPLETED": 2,
    "FAILED": -1
}

# Helper to sanitize environment variables or return fallbacks
def get_env_var(key: str, default: Any = None) -> Any:
    value = os.getenv(key)
    if value is None:
        return default
    # Attempt type inference for simple env variables
    if value.lower() in ("true", "yes", "1"): return True
    if value.lower() in ("false", "no", "0"): return False
    try:
        return int(value)
    except ValueError:
        return value

# Registry of system-wide character encoding standards
DEFAULT_ENCODING: Final[str] = "utf-8"
ALLOWED_EXTENSIONS: Final[set[str]] = {'.json', '.csv', '.txt', '.log'}