import enum
from typing import Any, Dict, Callable

class DataTransformer(enum.Enum):
    STRIP = str.strip
    UPPER = str.upper
    LOWER = str.lower
    TRIM_ZERO = lambda s: s.lstrip('0')

class Registry:
    """A magical bucket for data conversion functions."""
    _registry: Dict[str, Callable[[Any], Any]] = {}

    @classmethod
    def register(cls, key: str):
        def wrapper(func: Callable):
            cls._registry[key] = func
            return func
        return wrapper

    @classmethod
    def apply(cls, key: str, value: Any) -> Any:
        func = cls._registry.get(key, lambda x: x)
        return func(value)

@Registry.register('currency')
def clean_currency(val: Any) -> float:
    if isinstance(val, str):
        return float(val.replace('$', '').replace(',', ''))
    return float(val)

@Registry.register('bool_int')
def to_bool(val: Any) -> bool:
    return int(val) != 0

DEFAULT_CONFIG = {
    'encoding': 'utf-8',
    'max_retries': 3,
    'timeout': 30,
    'transformers': DataTransformer
}