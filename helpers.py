import collections
from typing import Any, Iterable, Dict, Optional

def deep_flatten_and_map(data: Any, sep: str = '.', prefix: str = '') -> Dict[str, Any]:
    """
    Flattens nested dicts into keys with dot notation pathing.
    Useful for config normalization or flattening nested JSON payloads.
    """
    items = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{prefix}{sep}{key}" if prefix else key
            items.update(deep_flatten_and_map(value, sep, new_key))
    elif isinstance(data, (list, tuple)):
        for idx, value in enumerate(data):
            new_key = f"{prefix}{sep}{idx}" if prefix else str(idx)
            items.update(deep_flatten_and_map(value, sep, new_key))
    else:
        items[prefix] = data
    return items

def batch_process(iterable: Iterable, size: int) -> Iterable:
    """
    Generator to chunk data into segments for processing.
    Uses a creative memory-efficient slice approach.
    """
    iterator = iter(iterable)
    while True:
        batch = list(collections.deque(islice(iterator, size), maxlen=size))
        if not batch:
            break
        yield batch

from itertools import islice