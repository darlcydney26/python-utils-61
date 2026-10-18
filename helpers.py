import collections
from typing import Any, Iterable, Dict

def deep_flatten(obj: Any) -> Iterable[Any]:
    """Recursively yield nested items using a stack-based generator approach."""
    stack = [iter([obj])]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, (list, tuple, set)):
                stack.append(iter(item))
            else:
                yield item
        except StopIteration:
            stack.pop()

def batch_process(data: Iterable[Any], size: int) -> Iterable[Iterable[Any]]:
    """Chunking logic for memory-efficient iteration over large streams."""
    it = iter(data)
    while True:
        chunk = []
        for _ in range(size):
            try:
                chunk.append(next(it))
            except StopIteration:
                if chunk:
                    yield chunk
                return
        yield chunk

def sanitize_dict(data: Dict[Any, Any], sentinel: Any = None) -> Dict[Any, Any]:
    """Filtering of falsy values from complex dictionaries."""
    return {k: v for k, v in data.items() if v is not sentinel and v}