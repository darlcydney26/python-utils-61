from typing import Any, Callable, Dict, List, Union


class PathDataProcessor:
    """Nested structure query and dynamic transformer using path notation."""

    def __init__(self, data: Any) -> None:
        self._data = data

    def extract(self, path: str, default: Any = None) -> Any:
        tokens = [t for t in path.strip("/").split("/") if t]
        curr = self._data
        for token in tokens:
            if isinstance(curr, dict) and token in curr:
                curr = curr[token]
            elif isinstance(curr, (list, tuple)) and token.isdigit():
                idx = int(token)
                curr = curr[idx] if 0 <= idx < len(curr) else default
            else:
                return default
        return curr

    def mutate(self, rules: Dict[str, Callable[[Any], Any]]) -> Any:
        def _walk(node: Any, current_path: str) -> Any:
            if current_path in rules:
                node = rules[current_path](node)

            if isinstance(node, dict):
                return {
                    k: _walk(v, f"{current_path}/{k}" if current_path else str(k))
                    for k, v in node.items()
                }
            elif isinstance(node, list):
                return [
                    _walk(item, f"{current_path}/{i}" if current_path else str(i))
                    for i, item in enumerate(node)
                ]
            return node

        return _walk(self._data, "")

    def __rshift__(self, step: Union[tuple, Dict[str, Callable[[Any], Any]]]) -> "PathDataProcessor":
        if isinstance(step, tuple) and len(step) == 2:
            rules = {step[0]: step[1]}
        elif isinstance(step, dict):
            rules = step
        else:
            raise ValueError("Invalid pipeline mutation specification")
        return PathDataProcessor(self.mutate(rules))

    @property
    def value(self) -> Any:
        return self._data
