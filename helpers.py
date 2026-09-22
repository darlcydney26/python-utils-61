import functools

def validate_loop_input(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for item in args[0] if args else []:
                for key, validator in schema.items():
                    if not validator(item.get(key)):
                        raise ValueError(f'invalid field: {key}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_non_empty_str(x):
    return isinstance(x, str) and len(x) > 0

def is_positive_int(x):
    return isinstance(x, int) and x > 0

@validate_loop_input({'name': is_non_empty_str, 'id': is_positive_int})
def run_processing_loop(data_packets):
    results = []
    for packet in data_packets:
        results.append(f"Processing {packet['name']} with id {packet['id']}")
    return results

if __name__ == '__main__':
    data = [{'name': 'alpha', 'id': 1}, {'name': 'beta', 'id': 2}]
    try:
        print(run_processing_loop(data))
    except ValueError as e:
        print(f'Validation failure: {e}')