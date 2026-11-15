import collections
import re
from typing import Any, Dict, List, Union

class DataAlchemy:
    """
    A collection of transformative rituals for mundane data structures.
    Utilizes recursive mutation to sanitize keys and normalize nested containers.
    """
    def __init__(self, key_transformer=lambda k: str(k).lower().replace(' ', '_')):
        self.transformer = key_transformer

    def transmute(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {self.transformer(k): self.transmute(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple, set)):
            return [self.transmute(i) for i in data]
        return data

    @staticmethod
    def extract_patterns(text: str, pattern: str = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}') -> List[str]:
        """Extracts specific data fragments using regex magic."""
        return re.findall(pattern, text)

    @staticmethod
    def flatten(mapping: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        items = []
        for k, v in mapping.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(DataAlchemy.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

ALCHEMY = DataAlchemy()