import functools
from typing import Any, Callable, Dict, List, Union

def cast_structure(data: Any, schema: Dict[type, Callable]) -> Any:
    """Recursively apply transformation functions to data structures."""
    if isinstance(data, dict):
        return {k: cast_structure(v, schema) for k, v in data.items()}
    if isinstance(data, list):
        return [cast_structure(item, schema) for item in data]
    
    for target_type, transform in schema.items():
        if isinstance(data, target_type):
            return transform(data)
    return data

def deep_flatten(obj: Union[List, Dict]) -> List[Any]:
    """Generator-based recursive flattening of nested collections."""
    items = obj.values() if isinstance(obj, dict) else obj
    result = []
    for item in items:
        if isinstance(item, (list, dict)):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def memoize_data(func: Callable) -> Callable:
    """Local cache decorator for static data transformations."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def get_path(data: Dict, path: str, default: Any = None) -> Any:
    """Dot-notation navigation through nested dictionary objects."""
    try:
        return functools.reduce(lambda d, key: d[key], path.split('.'), data)
    except (KeyError, TypeError, AttributeError):
        return default