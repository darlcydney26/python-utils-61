from typing import Any, Callable, Dict, List, Union

class DataMorpher:
    """A lightweight, operator-driven data transformer for nested dictionaries."""
    
    def __init__(self, data: Union[Dict, List]):
        self._data = data

    @property
    def raw(self) -> Any:
        return self._data

    def __rshift__(self, func: Callable[[Any], Any]) -> "DataMorpher":
        """Overloads `>>` operator to apply a transformation function recursively."""
        def _apply(val):
            if isinstance(val, dict):
                return {k: _apply(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [_apply(v) for v in val]
            return func(val)
        return DataMorpher(_apply(self._data))

    def __getitem__(self, key_path: str) -> Any:
        """Access deeply nested keys using dot notation like `morpher['a.b.c']`."""
        keys = key_path.split('.')
        curr = self._data
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            elif isinstance(curr, list) and k.isdigit() and int(k) < len(curr):
                curr = curr[int(k)]
            else:
                return None
        return curr

    def flatten(self, separator: str = ".") -> Dict[str, Any]:
        """Flattens a nested dictionary or list hierarchy into single-level dict."""
        out = {}
        def _flatten(obj, prefix=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    _flatten(v, f"{prefix}{k}{separator}" if prefix else f"{k}{separator}")
            elif isinstance(obj, list):
                for idx, v in enumerate(obj):
                    _flatten(v, f"{prefix}{idx}{separator}" if prefix else f"{idx}{separator}")
            else:
                out[prefix.rstrip(separator)] = obj
        _flatten(self._data)
        return out

def process_nested_payload(payload: Dict[str, Any], transformations: List[Callable]) -> Dict[str, Any]:
    """Helper function to run morph pipelines on standard dictionaries."""
    morpher = DataMorpher(payload)
    for transform in transformations:
        morpher = morpher >> transform
    return morpher.raw
