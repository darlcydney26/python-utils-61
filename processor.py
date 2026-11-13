import functools
import collections

class DataProcessor:
    def __init__(self, cache_size=1024):
        self._cache_size = cache_size
        self._memo = {}
        self._order = collections.deque()

    def process_heavy_transform(self, data: bytes) -> bytes:
        """Implements a custom LRU-style cache using an unusual dictionary-deque hybrid."""
        if data in self._memo:
            self._order.remove(data)
            self._order.append(data)
            return self._memo[data]
        
        result = self._execute_computation(data)
        
        if len(self._memo) >= self._cache_size:
            oldest = self._order.popleft()
            del self._memo[oldest]
        
        self._memo[data] = result
        self._order.append(data)
        return result

    def _execute_computation(self, data: bytes) -> bytes:
        # Simulated compute-intensive operation
        return bytes(reversed(data))

    def batch_process(self, data_list: list[bytes]) -> list[bytes]:
        """Vectorized-style processing wrapper for throughput optimization."""
        return [self.process_heavy_transform(d) for d in data_list]

    def __repr__(self):
        return f"<Processor: {len(self._memo)} cached entries>"