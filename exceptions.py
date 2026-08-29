import functools
from typing import Any, Callable

class AppException(Exception):
    def __init__(self, message: str, error_code: int = 500):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class ResourceNotFoundException(AppException):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404)

def exception_handler(default_return: Any = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except AppException as e:
                print(f"Handled {type(e).__name__}: {e.message} (code: {e.error_code})")
                return default_return
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return default_return
        return wrapper
    return decorator

@exception_handler(default_return=0)
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValidationException("Division by zero not allowed")
    return a / b

@exception_handler(default_return=None)
def get_resource(name: str) -> str:
    if not name:
        raise ValidationException("Name cannot be empty")
    if name == "missing":
        raise ResourceNotFoundException(name)
    return f"Data for {name}"

def retry_on_exception(max_attempts: int = 3) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Retrying after exception: {type(e).__name__}")
            if last_exception:
                raise last_exception
            return None
        return wrapper
    return decorator

@retry_on_exception(max_attempts=3)
def fetch_data():
    import random
    if random.random() < 0.7:
        raise AppException("Temporary failure", 503)
    return {"data": "success"}

def map_to_custom_exception(error: Exception) -> AppException:
    if isinstance(error, ZeroDivisionError):
        return ValidationException("Attempted division by zero")
    if isinstance(error, FileNotFoundError):
        return ResourceNotFoundException("requested file")
    return AppException(str(error), 500)