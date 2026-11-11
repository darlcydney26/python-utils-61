import functools
from typing import Callable, Any, Dict, List, Tuple


class HelperRegistry(type):
    """Metaclass for automatic registration and chaining of helper functions."""

    _helpers: Dict[str, Callable] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        for attr_name, attr_val in namespace.items():
            if callable(attr_val) and not attr_name.startswith("_"):
                mcs._helpers[attr_name] = attr_val
        return cls

    @classmethod
    def get_pipeline(cls, *names: str) -> Callable:
        funcs = [cls._helpers[n] for n in names if n in cls._helpers]

        def runner(initial_val: Any) -> Any:
            res = initial_val
            for f in funcs:
                res = f(res)
            return res

        return runner


class CoreHelpers(metaclass=HelperRegistry):
    """Collection of reusable data sanitization and transformation helpers."""

    @staticmethod
    def strip_whitespace(val: Any) -> Any:
        return val.strip() if isinstance(val, str) else val

    @staticmethod
    def sanitize_keys(data: Any) -> Any:
        if isinstance(data, dict):
            return {str(k).lower().replace(" ", "_"): v for k, v in data.items()}
        return data

    @staticmethod
    def flatten_nested(data: Any) -> Any:
        if not isinstance(data, (list, tuple)):
            return [data]
        flat = []
        for item in data:
            if isinstance(item, (list, tuple)):
                flat.extend(CoreHelpers.flatten_nested(item))
            else:
                flat.append(item)
        return flat


def create_chain(*steps: str) -> Callable[[Any], Any]:
    """Utility wrapper to build dynamic helper transformation pipelines."""
    return HelperRegistry.get_pipeline(*steps)
