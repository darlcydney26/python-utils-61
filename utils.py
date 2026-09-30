from typing import Any, Union, List, Dict

class PathNavigator:
    """
    A creative utility for traversing nested dictionary and list structures
    using filesystem-like path syntax, including relative backtracks (..) and wildcards (*).
    """
    def __init__(self, data: Union[Dict, List]):
        self.data = data

    def _parse(self, path: str) -> List[str]:
        return [s for s in path.split('/') if s and s != '.']

    def get(self, path: str, default: Any = None) -> Any:
        if not path or path == '/':
            return self.data

        segments = self._parse(path)
        state = [([], self.data)]

        for step in segments:
            next_state = []
            for history, current in state:
                if step == '..':
                    if history:
                        parent_history = history[:-1]
                        parent_val = self.data
                        for key in parent_history:
                            if isinstance(parent_val, list