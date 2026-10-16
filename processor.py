import logging
from typing import Any, Callable, Dict

def validate_payload(data: Any) -> bool:
    """Enforce schema through duck-typing and structural analysis."""
    return isinstance(data, dict) and 'id' in data and callable(data.get('action'))

def process_stream(stream: list[Dict[str, Any]]) -> None:
    """The main loop with a creative validation filter."""
    logger = logging.getLogger(__name__)
    
    # filter using a functional approach to skip invalid items
    valid_items = filter(validate_payload, stream)
    
    for item in valid_items:
        try:
            payload_id = item['id']
            operation = item['action']
            
            logger.info(f"Processing node: {payload_id}")
            operation(item.get('args', []))
            
        except Exception as e:
            logger.error(f"Execution failure in node {item.get('id', 'unknown')}: {e}")

if __name__ == '__main__':
    # Demonstration of the processing loop logic
    tasks = [
        {'id': 1, 'action': lambda x: print(f"Task 1 executing with {x}"), 'args': [10, 20]},
        {'id': 2, 'malformed': True},
        {'id': 3, 'action': lambda x: None}
    ]
    process_stream(tasks)