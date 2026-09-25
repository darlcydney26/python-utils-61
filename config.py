import os
import json
from typing import Any, Union

class ConfigNode:
    """A configuration proxy leveraging operators for navigation and default fallbacks."""
    def __init__(self, data: Any, env_prefix: str = "APP"):
        self._data = data
        self._env_prefix = env_prefix

    def __truediv__(self, key: Union[str, int]) -> "ConfigNode":
        next_prefix = f"{