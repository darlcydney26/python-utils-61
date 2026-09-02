class CoreOptimizer:
    def __init__(self, max_cache_size=100):
        self._cache = {}
        self._max_cache_size = max_cache_size
        self._access_order = []
    def _evict(self):
        if len(self._cache) > self._max_cache_size:
            oldest = self._access_order.pop(0)
            if oldest in self._cache:
                del self._cache[oldest]
    def cached_call(self, func, *args):
        key = (func.__name__, args)
        if key in self._cache:
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        result = func(*args)
        self._cache[key] = result
        self._access_order.append(key)
        self._evict()
        return result
    def optimized_sum(self, data):
        total = 0
        for item in data:
            total += item
        return total
    def optimized_filter(self, data, condition):
        return [item for item in data if condition(item)]
    def process_batch(self, items, func):
        results = []
        for item in items:
            results.append(self.cached_call(func, item))
        return results
    def optimized_product(self, data):
        if not data:
            return 1
        prod = 1
        for item in data:
            prod *= item
        return prod
    def vector_add(self, vec1, vec2):
        return [a + b for a, b in zip(vec1, vec2)]
    def matrix_multiply(self, mat1, mat2):
        if not mat1 or not mat2 or not mat1[0] or not mat2[0]:
            return []
        rows = len(mat1)
        cols = len(mat2[0])
        result = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                for k in range(len(mat2)):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return result