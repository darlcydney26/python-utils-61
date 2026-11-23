import logging
import functools

class DataValidator:
    """Validator acting as a guard for the processing stream."""
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(data):
            if not all(k in data for k in self.schema):
                logging.error(f"Invalid packet schema: {data.keys()}")
                return None
            return func(data)
        return wrapper

logger = logging.getLogger('python-utils-61')
logging.basicConfig(level=logging.INFO)

@DataValidator(['id', 'payload'])
def process_event(data):
    logger.info(f"Processing event {data['id']}: {data['payload']}")
    return True

def run_event_loop(events):
    """Execution loop with integrated validation checks."""
    for event in events:
        if process_event(event):
            logger.debug("Event handled successfully")
        else:
            logger.warning("Dropping malformed event packet")

if __name__ == '__main__':
    mock_events = [
        {'id': 1, 'payload': 'init'},
        {'corrupt': 'data'},
        {'id': 2, 'payload': 'shutdown'}
    ]
    run_event_loop(mock_events)