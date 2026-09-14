from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain callables into a single functional pipeline."""
    def pipeline(data: Any) -> Any:
        for func in funcs:
            data = func(data)
        return data
    return pipeline

def dict_deep_merge(base: Dict[Any, Any], update: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursive dictionary merging for nested config structures."""
    for key, value in update.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            dict_deep_merge(base[key], value)
        else:
            base[key] = value
    return base

def flatten_list(nested: List[Any]) -> List[Any]:
    """Generator-based flattening of arbitrarily nested iterables."""
    result: List[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def batch_process(items: List[T], size: int) -> List[List[T]]:
    """Slicing logic for memory-efficient chunked iteration."""
    return [items[i:i + size] for i in range(0, len(items), size)]