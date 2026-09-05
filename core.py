import types
from typing import Callable, Any, List, Iterable


class UnrolledPipeline:
    """Dynamic code generator for unrolled functional pipeline execution."""

    def __init__(self, steps: List[Callable[[Any], Any]] = None):
        self.steps = steps or []
        self._compiled_runner = self._build_unrolled_runner()

    def _build_unrolled_runner(self) -> Callable[[Any], Any]:
        if not self.steps:
            return lambda x: x

        env = {f"_fn_{i}": fn for i, fn in enumerate(self.steps)}
        lines = ["def _runner(val):"]
        for i in range(len(self.steps)):
            lines.append(f"    val = _fn_{i}(val)")
        lines.append("    return val")

        source = "\n".join(lines)
        code_obj = compile(source, "<unrolled_pipeline>", "exec")
        local_scope = {}
        exec(code_obj, env, local_scope)
        return local_scope["_runner"]

    def __call__(self, initial_value: Any) -> Any:
        return self._compiled_runner(initial_value)

    def add_step(self, step: Callable[[Any], Any]) -> "UnrolledPipeline":
        self.steps.append(step)
        self._compiled_runner = self._build_unrolled_runner()
        return self


class CoreEngine:
    """High-performance core execution engine with batch processing capabilities."""

    __slots__ = ("_pipeline",)

    def __init__(self):
        self._pipeline = UnrolledPipeline()

    def add_transform(self, func: Callable[[Any], Any]) -> "CoreEngine":
        self._pipeline.add_step(func)
        return self

    def process_batch(self, items: Iterable[Any]) -> list:
        runner = self._pipeline
        return [runner(item) for item in items]
