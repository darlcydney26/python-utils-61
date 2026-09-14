import functools

def validate_inputs(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, validator in schema.items():
                value = kwargs.get(key)
                if value is not None and not validator(value):
                    raise ValueError(f'invalid input for {key}: {value}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_positive(x):
    return isinstance(x, (int, float)) and x > 0

def is_non_empty_str(x):
    return isinstance(x, str) and len(x) > 0

def process_main_loop(data_stream):
    """
    Main processing loop with declarative validation
    """
    schema = {
        'id': is_positive,
        'payload': is_non_empty_str
    }

    @validate_inputs(schema)
    def handle_item(item_id, payload):
        return f'processed {item_id}: {payload}'

    results = []
    for entry in data_stream:
        try:
            results.append(handle_item(id=entry.get('id'), payload=entry.get('payload')))
        except (ValueError, TypeError) as e:
            print(f'skipping malformed entry: {e}')
    return results