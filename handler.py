import itertools
from typing import Any, Callable, Dict, List, Optional, Union

def safe_divide(a: Union[int, float], b: Union[int, float], default: float = 0.0) -> float:
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def flatten_nested(data: Any, depth: Optional[int] = None) -> List[Any]:
    if not isinstance(data, (list, tuple)):
        return [data]
    result = []
    stack = [(data, 0)]
    while stack:
        current, d = stack.pop()
        if isinstance(current, (list, tuple)) and (depth is None or d < depth):
            for item in reversed(current):
                stack.append((item, d + 1))
        else:
            result.append(current)
    return result[::-1]

def batch_process(items: List[Any], batch_size: int = 10) -> List[List[Any]]:
    if batch_size <= 0:
        return [items]
    it = iter(items)
    batches = []
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        batches.append(batch)
    return batches

def deep_update(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in update.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            base[key] = deep_update(base[key], value)
        else:
            base[key] = value
    return base

def unique_with_order(seq: List[Any]) -> List[Any]:
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def handle_common(data: Any, op: str, **kwargs: Any) -> Any:
    ops: Dict[str, Callable[[Any], Any]] = {
        "flatten": lambda d: flatten_nested(d, kwargs.get("depth")),
        "batch": lambda d: batch_process(d, kwargs.get("size", 10)),
        "unique": unique_with_order,
        "safe_div": lambda d: safe_divide(d[0], d[1]) if isinstance(d, (list, tuple)) and len(d) > 1 else d,
        "merge": lambda d: deep_update(d[0], d[1]) if isinstance(d, (list, tuple)) and len(d) > 1 else d,
    }
    handler = ops.get(op)
    if handler:
        return handler(data)
    return data