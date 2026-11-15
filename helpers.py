from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def morph_list(data: List[Any], func: Callable[[Any], T]) -> List[T]:
    """
    Applies a transformation function to each element in a list.
    
    Args:
        data: A list of arbitrary elements.
        func: A callable to transform individual items.
        
    Returns:
        A list containing the transformed elements.
    """
    return [func(item) for item in data]

def dict_shredder(target: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Extracts a subset of key-value pairs from a dictionary.
    
    Args:
        target: The source dictionary to extract from.
        keys: A list of keys to filter by.
        
    Returns:
        A new dictionary containing only the specified keys if present.
    """
    return {k: target[k] for k in keys if k in target}

def flip_bit_logic(val: Union[int, bool]) -> bool:
    """
    Forces a boolean inversion of any integer or boolean input.
    
    Args:
        val: The input value to flip.
        
    Returns:
        The logical negation of the input truthiness.
    """
    return not bool(val)

class DataEnvelope:
    """
    A wrapper for metadata-enriched payloads.
    """
    def __init__(self, payload: Any, metadata: Dict[str, str]) -> None:
        self.payload = payload
        self.metadata = metadata

    def reveal(self) -> Any:
        return self.payload