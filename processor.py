import functools
from typing import Any, Callable, Dict, List


class PipelineStage:
    def __init__(self, name: str, transform: Callable[[Any], Any]):
        self.name = name
        self.transform = transform

    def __call__(self, data: Any) -> Any:
        return self.transform(data)


class DataProcessor:
    """Dynamic dataset reorganization and cleanup utility pipeline."""

    def __init__(self) -> None:
        self._stages: List[PipelineStage] = []

    def register(self, name: str | None = None):
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            stage_name = name or func.__name__
            self._stages.append(PipelineStage(stage_name, func))

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = payload.copy()
        for stage in self._stages:
            result = stage(result)
        return result

    def sanitize_keys(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            str(k).strip().lower().replace(" ", "_"): v
            for k, v in data.items()
            if v is not None
        }


def compose_cleanup(*transforms: Callable[[Dict[str, Any]], Dict[str, Any]]):
    def pipeline(initial: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(initial)
        for xform in transforms:
            state = xform(state)
        return state

    return pipeline


def prune_empty(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v not in ("", None, [], {}, set())}


def normalize_numeric_strings(data: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in data.items():
        if isinstance(v, str) and v.isdigit():
            out[k] = int(v)
        else:
            out[k] = v
    return out
