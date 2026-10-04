from typing import Any, Callable, Union


class FluentDataHandler:
    """Creative wrapper enabling chainable path querying and functional mutations on nested data."""

    def __init__(self, data: Any = None):
        self._data = data

    def __getitem__(self, path: Union[str, int]) -> "FluentDataHandler":
        if isinstance(path, int):
            if isinstance(self._data, (list, tuple)) and 0 <= path < len(self._data):
                return FluentDataHandler(self._data[path])
            return FluentDataHandler(None)

        if not isinstance(path, str) or self._data is None:
            return FluentDataHandler(None)

        curr = self._data
        for part in path.split("."):
            if part == "*" and isinstance(curr, (list, tuple)):
                return FluentDataHandler([FluentDataHandler(x) for x in curr])
            if isinstance(curr, dict):
                curr = curr.get(part)
            elif isinstance(curr, (list, tuple)) and part.isdigit():
                curr = curr[int(part)]
            elif isinstance(curr, list) and all(isinstance(x, FluentDataHandler) for x in curr):
                curr = [x[part]._data for x in curr]
            else:
                return FluentDataHandler(None)
        return FluentDataHandler(curr)

    def map(self, fn: Callable[[Any], Any]) -> "FluentDataHandler":
        if isinstance(self._data, list):
            extracted = [item.unwrap() if isinstance(item, FluentDataHandler) else item for item in self._data]
            return FluentDataHandler([fn(elem) for elem in extracted])
        return FluentDataHandler(fn(self._data) if self._data is not None else None)

    def filter(self, predicate: Callable[[Any], bool]) -> "FluentDataHandler":
        if isinstance(self._data, list):
            items = [item.unwrap() if isinstance(item, FluentDataHandler) else item for item in self._data]
            return FluentDataHandler([x for x in items if predicate(x)])
        return self if predicate(self._data) else FluentDataHandler(None)

    def fold(self, initial: Any, accumulator: Callable[[Any, Any], Any]) -> Any:
        raw = self.unwrap()
        if not isinstance(raw, (list, tuple, set)):
            return accumulator(initial, raw)
        res = initial
        for val in raw:
            res = accumulator(res, val)
        return res

    def unwrap(self) -> Any:
        if isinstance(self._data, list):
            return [x.unwrap() if isinstance(x, FluentDataHandler) else x for x in self._data]
        return self._data


def handle_data(data: Any) -> FluentDataHandler:
    return FluentDataHandler(data)
