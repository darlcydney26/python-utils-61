import functools
from typing import Any, Callable, Dict, List, Tuple


class FastPipeline:
    """Core fast-path execution pipeline with step-unrolling call caches."""

    __slots__ = ("_steps", "_cache", "_maxsize", "_compiled_path")

    def __init__(self, maxsize: int = 512):
        self._steps: List[Callable[[Any], Any]] = []
        self._cache: Dict[Tuple[int, int], Any] = {}
        self._maxsize = maxsize
        self._compiled_path: Callable[[Any], Any] | None = None

    def pipe(self, fn: Callable[[Any], Any]) -> "FastPipeline":
        self._steps.append(fn)
        self._compiled_path = None
        return self

    def _compile(self) -> Callable[[Any], Any]:
        if not self._steps:
            return lambda x: x
        steps = tuple(self._steps)

        def compiled(val: Any) -> Any:
            for step in steps:
                val = step(val)
            return val

        self._compiled_path = compiled
        return compiled

    def execute(self, items: List[Any]) -> List[Any]:
        runner = self._compiled_path or self._compile()
        cache = self._cache
        maxsize = self._maxsize
        results = []

        for item in items:
            key = (id(type(item)), hash(item)) if isinstance(item, (int, str, float, tuple)) else None
            if key is not None and key in cache:
                results.append(cache[key])
                continue

            res = runner(item)
            if key is not None:
                if len(cache) >= maxsize:
                    cache.clear()
                cache[key] = res
            results.append(res)

        return results

    def flush(self) -> None:
        self._cache.clear()
        self._compiled_path = None
