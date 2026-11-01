import functools

class ValidationError(Exception):
    pass

def validate_loop(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for item in args[0] if args else []:
                for key, validator in schema.items():
                    value = item.get(key)
                    if not validator(value):
                        raise ValidationError(f"Invalid {key}: {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_non_empty_str(x):
    return isinstance(x, str) and len(x) > 0

def is_positive_int(x):
    return isinstance(x, int) and x > 0

@validate_loop({"name": is_non_empty_str, "id": is_positive_int})
def process_data(batch):
    results = []
    for entry in batch:
        results.append(f"Processing {entry['name']} ({entry['id']})")
    return results

if __name__ == "__main__":
    data = [{"name": "task_1", "id": 1}, {"name": "task_2", "id": 2}]
    try:
        print(process_data(data))
    except ValidationError as e:
        print(f"Validation failure: {e}")