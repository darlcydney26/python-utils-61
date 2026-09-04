from typing import TypeVar, Iterable, Any, Callable, List

T = TypeVar('T')

def batch_process(iterable: Iterable[T], size: int, func: Callable[[List[T]], Any] = list) -> List[Any]:
    """
    partitioning of streams into chunks of arbitrary types.

    :param iterable: source data to be chunked.
    :param size: integer defining the maximum chunk length.
    :param func: transformation applied to each resultant batch.
    :return: list of processed batch results.
    """
    items = list(iterable)
    return [func(items[i:i + size]) for i in range(0, len(items), size)]

def recursive_map(data: Any, transformer: Callable[[Any], Any]) -> Any:
    """
    depth-first traversal and modification of nested structures.

    :param data: nested dictionary or list container.
    :param transformer: callback function for modifying leaves.
    :return: transformed structure with preserved hierarchy.
    """
    if isinstance(data, dict):
        return {k: recursive_map(v, transformer) for k, v in data.items()}
    elif isinstance(data, list):
        return [recursive_map(i, transformer) for i in data]
    return transformer(data)