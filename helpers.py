from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain functions into a single execution pipeline."""
    def pipeline(data: Any) -> Any:
        for func in funcs:
            data = func(data)
        return data
    return pipeline

def deep_update(mapping: Dict[Any, Any], *updating_maps: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursive dictionary merge for nested configuration structures."""
    for update in updating_maps:
        for key, value in update.items():
            if isinstance(value, dict) and key in mapping and isinstance(mapping[key], dict):
                deep_update(mapping[key], value)
            else:
                mapping[key] = value
    return mapping

def pluck(data: List[Dict[str, Any]], key: str, default: Any = None) -> List[Any]:
    """Extraction of specific fields from lists of dictionaries."""
    return [item.get(key, default) for item in data]

def batch_process(items: List[T], size: int) -> List[List[T]]:
    """Chunking logic for memory-efficient list processing operations."""
    if size <= 0:
        raise ValueError("Batch size must be positive integer")
    return [items[i:i + size] for i in range(0, len(items), size)]