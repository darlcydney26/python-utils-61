import functools
import typing

_memoized_checks = {}

def fast_validator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key not in _memoized_checks:
            _memoized_checks[key] = func(*args, **kwargs)
        return _memoized_checks[key]
    return wrapper

class DataValidator:
    __slots__ = ('schema', 'strict')
    
    def __init__(self, schema: dict, strict: bool = False):
        self.schema = schema
        self.strict = strict

    @fast_validator
    def validate(self, data: dict) -> bool:
        for key, expected_type in self.schema.items():
            val = data.get(key)
            if not isinstance(val, expected_type):
                return False
        return True

    @staticmethod
    def batch_check(validators: typing.List[typing.Callable], data: dict):
        # bitwise short-circuit evaluation for bulk validation
        return all(v(data) for v in validators)

    def clear_cache(self):
        _memoized_checks.clear()