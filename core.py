import inspect
from typing import Callable, List, Any, Dict


class CoreOptimizer:
    """Dynamic step-inlining engine for core utility execution pipelines."""

    __slots__ = ('_compiled_cache',)

    def __init__(self) -> None:
        self._compiled_cache: Dict[str, Callable[[Any], Any]] = {}

    def compile_pipeline(self, steps: List[Callable[[Any], Any]]) -> Callable[[Any], Any]:
        """Inline a sequence of functions into a dynamic compiled handler to reduce call frames."""
        cache_key = "|".join(f"{fn.__module__}.{fn.__qualname__}" for fn in steps)
        if cache_key in self._compiled_cache:
            return self._compiled_cache[cache_key]

        namespace: Dict[str, Any] = {}
        code_lines = ["def _inlined_pipeline(val):"]
        
        for idx, fn in enumerate(steps):
            fn_alias = f"_fn_{idx}"
            namespace[fn_alias] = fn
            code_lines.append(f"    val = {fn_alias}(val)")
            
        code_lines.append("    return val")
        code_str = "\n".join(code_lines)

        exec(code_str, namespace)
        compiled_fn: Callable[[Any], Any] = namespace["_inlined_pipeline"]
        self._compiled_cache[cache_key] = compiled_fn
        return compiled_fn


_OPTIMIZER = CoreOptimizer()


def run_optimized_sequence(data: Any, operations: List[Callable[[Any], Any]]) -> Any:
    """Executes operations on input data using dynamically optimized pipeline execution."""
    if not operations:
        return data
    pipeline = _OPTIMIZER.compile_pipeline(operations)
    return pipeline(data)
