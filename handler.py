import sys
from typing import Any, Callable, Generator, Iterable, Dict

class ValidationError(ValueError):
    pass

class LoopHandler:
    def __init__(self, schemas: Dict[str, Callable[[Any], bool]]):
        self.schemas = schemas

    def process(self, items: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for index, item in enumerate(items):
            try:
                if not isinstance(item, dict):
                    raise ValidationError('Item is not a dictionary structure')
                
                for key, validator in self.schemas.items():
                    if key not in item:
                        raise ValidationError(f'Missing required field: {key}')
                    if not validator(item[key]):
                        raise ValidationError(f'Validation failed for \'{key}\': {item[key]}')
                
                yield {
                    'id': index,
                    'payload': {k: v for k, v in item.items() if not k.startswith('_')},
                    'valid': True
                }
            except ValidationError as exc:
                yield {
                    'id': index,
                    'error': str(exc),
                    'valid': False
                }