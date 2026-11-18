import collections
from typing import Any, Iterable, Dict, Union

class DataTransformer:
    """A magical recursive container transformer for unpredictable schemas."""
    def __init__(self, key_transformer=str.lower):
        self.kt = key_transformer

    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {self.kt(k): self.process(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple, set)):
            return [self.process(item) for item in data]
        return data

def batch_iterator(data: Iterable, chunk_size: int = 10):
    """Generator for chunking collections with a twist."""
    it = iter(data)
    chunk = list(next(it, None) for _ in range(chunk_size))
    while any(chunk):
        yield [x for x in chunk if x is not None]
        chunk = list(next(it, None) for _ in range(chunk_size))

def deep_flatten(nested: Any) -> Iterable:
    """Flattens arbitrary nested structures into a stream."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from deep_flatten(item)
        else:
            yield item

if __name__ == '__main__':
    transformer = DataTransformer()
    sample = {'UserID': 1, 'META': {'Tags': ['Python', 'Dev']}}
    print(transformer.process(sample))