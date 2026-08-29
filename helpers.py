import functools
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar('T')

def safe_get(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """Get nested value using reduce for creative path traversal"""
    try:
        return functools.reduce(
            lambda d, k: d.get(k) if isinstance(d, dict) else None, 
            keys, 
            data
        ) or default
    except (AttributeError, TypeError):
        return default

def chunk_list(data: List[T], size: int) -> List[List[T]]:
    """Recursive chunking for unusual list partitioning"""
    if not data or size <= 0:
        return []
    return [data[:size]] + chunk_list(data[size:], size)

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Iterative flatten with stack for creative approach"""
    items = []
    stack = [(d, parent_key)]
    while stack:
        current, prefix = stack.pop()
        for k, v in current.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, dict):
                stack.append((v, new_key))
            else:
                items.append((new_key, v))
    return dict(items)

def retry_with_backoff(max_attempts: int = 3, backoff_factor: float = 0.1) -> Callable:
    """Decorator with exponential backoff using unusual timing"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(backoff_factor * (2 ** attempt))
            return None
        return wrapper
    return decorator

def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive merge with copy for unusual combination"""
    result = dict1.copy()
    for k, v in dict2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

def get_unique_preserved(items: List[T], key_func: Optional[Callable[[T], Any]] = None) -> List[T]:
    """Unique items using dict for order preservation creatively"""
    if key_func is None:
        return list(dict.fromkeys(items))
    seen: Dict[Any, bool] = {}
    result: List[T] = []
    for item in items:
        k = key_func(item)
        if k not in seen:
            seen[k] = True
            result.append(item)
    return result