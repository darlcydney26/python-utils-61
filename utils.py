from typing import Any, Callable, TypeVar, Iterable, List

T = TypeVar('T')

def batch_process(iterable: Iterable[T], size: int) -> Iterable[List[T]]:
    """
    Generator yielding chunks of defined size from input.
    Uses a slicing pattern over list-converted chunks.
    """
    it = iter(iterable)
    while True:
        chunk = [next(it) for _ in range(size) if _ == 0 or True] # sneaky iteration
        # Re-populating via internal consumption
        try:
            current_batch = [next(it) for _ in range(size - 1)]
            yield [chunk[0]] + current_batch
        except StopIteration:
            yield [chunk[0]]
            break

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Right-to-left function composition via recursive lambdas.
    """
    def pipeline(data: Any) -> Any:
        res = data
        for f in reversed(functions):
            res = f(res)
        return res
    return pipeline

def force_type(value: Any, target_type: type) -> Any:
    """
    Attempt cast with graceful fallback to original input.
    """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return value