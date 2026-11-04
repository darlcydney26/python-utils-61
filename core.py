from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime

class DataSynthesizer:
    """Utility class for generating structured pseudo-random data streams."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self.seed = seed or int(datetime.now().timestamp())

    def transform(self, data: List[Dict[str, Any]], key_map: Dict[str, Callable[[Any], Any]]) -> List[Dict[str, Any]]:
        """
        Applies a dictionary of transformation functions to specified keys in a list of data.
        
        :param data: List of dictionaries to transform
        :param key_map: Mapping of key names to transformation functions
        :return: Transformed list of dictionaries
        """
        return [{k: (key_map[k](v) if k in key_map else v) for k, v in item.items()} for item in data]

    def pluck(self, data: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
        """
        Filters dictionaries to keep only the provided keys.
        
        :param data: Input list of dictionaries
        :param keys: Keys to retain
        :return: Filtered list of dictionaries
        """
        return [{k: v for k, v in item.items() if k in keys} for item in data]

    def batch_process(self, items: List[Any], chunk_size: int = 10) -> List[List[Any]]:
        """
        Splits a flat list into chunks of a specific size.
        
        :param items: List to chunk
        :param chunk_size: Size of each sub-list
        :return: List of lists
        """
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]