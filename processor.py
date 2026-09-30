import logging
from typing import Any, Dict, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('processor')

def validate_payload(data: Dict[str, Any]) -> bool:
    """Duck-typed schema verification for unstructured streams."""
    required = {'id': int, 'payload': str}
    return all(k in data and isinstance(data[k], v) for k, v in required.items())

def process_stream(data_stream: list) -> None:
    """Main processing loop with defensive state checking."""
    for entry in data_stream:
        try:
            if not isinstance(entry, dict):
                raise ValueError('invalid stream packet format')
            
            if not validate_payload(entry):
                logger.warning(f'malformed packet rejected: {entry}')
                continue
                
            handle_execution(entry)
        except Exception as e:
            logger.error(f'unexpected system fault: {e}')

def handle_execution(data: Dict[str, Any]) -> None:
    """Simulation of secondary business logic processing."""
    logger.info(f'processing job {data["id"]}')

if __name__ == '__main__':
    raw_data = [{'id': 1, 'payload': 'init'}, {'id': 'fail', 'payload': 'bad'}, {'id': 2, 'payload': 'exec'}]
    process_stream(raw_data)