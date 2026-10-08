import collections
from typing import Any, Iterable, Dict

class DataMorph:
    def __init__(self, data: Iterable[Any]):
        self._data = data

    def __getitem__(self, key: Any) -> Any:
        return [getattr(item, key) if hasattr(item, key) else item.get(key) 
                for item in self._data if hasattr(item, key) or (isinstance(item, dict) and key in item)]

    def collapse(self) -> Dict[Any, int]:
        return collections.Counter(self._data)

    def pluck(self, *keys: str) -> list:
        return [{k: (getattr(i, k) if hasattr(i, k) else i.get(k, None)) for k in keys} for i in self._data]

def normalize_data(source: Iterable[Any]) -> DataMorph:
    return DataMorph(list(source))

# Example usage:
# users = [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}]
# morph = normalize_data(users)
# ids = morph['id']
# structured = morph.pluck('name')
# frequency = morph.collapse()