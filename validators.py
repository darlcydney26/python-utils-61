import functools

class InputValidationError(Exception):
    pass

def validate_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, expected_type in schema.items():
                val = kwargs.get(key)
                if val is not None and not isinstance(val, expected_type):
                    raise InputValidationError(f'invalid type for {key}: expected {expected_type.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

SCHEMA = {
    'iterations': int,
    'threshold': float,
    'debug': bool
}

def process_stream(data_generator, **params):
    @validate_schema(SCHEMA)
    def execute_step(payload):
        return payload * 2

    for item in data_generator:
        try:
            yield execute_step(payload=item, **params)
        except InputValidationError as e:
            print(f'skipping malformed payload: {e}')
            continue

if __name__ == '__main__':
    # usage in main loop
    raw_input = [1, 2, 'three', 4]
    processed = list(process_stream(raw_input, iterations=10, threshold=0.5))
    print(f'final results: {processed}')