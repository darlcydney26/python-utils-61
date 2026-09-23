import logging

def validate_payload(data):
    if not isinstance(data, dict):
        raise ValueError('payload must be a dictionary')
    if 'id' not in data:
        raise KeyError('missing required identifier')
    return True

def process_stream(data_stream):
    logger = logging.getLogger(__name__)
    for entry in data_stream:
        try:
            validate_payload(entry)
            result = entry.get('value', 0) * 2
            logger.info(f'processed {entry["id"]}: {result}')
        except (ValueError, KeyError) as e:
            logger.warning(f'skipping malformed entry: {e}')
        except Exception:
            logger.error('unexpected pipeline corruption', exc_info=True)
            continue

if __name__ == '__main__':
    sample_data = [{'id': 1, 'value': 10}, {'error': 'bad'}, {'id': 2, 'value': 20}]
    process_stream(sample_data)