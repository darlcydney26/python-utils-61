from typing import Any, Callable, Dict, List, Union

class DataPipeline:
    def __init__(self, data: Any):
        self.data = data

    def transform(self, *funcs: Callable[[Any], Any]) -> 'DataPipeline':
        for f in funcs:
            try:
                self.data = f(self.data)
            except Exception as e:
                self.data = None
                break
        return self

    def get(self) -> Any:
        return self.data

def sanitize(val: Any) -> Any:
    if isinstance(val, str):
        return val.strip().lower()
    return val

def to_list(val: Any) -> List[Any]:
    return [val] if not isinstance(val, (list, tuple)) else list(val)

def apply_schema(data: Union[Dict, List], schema: Dict[str, Callable]) -> Dict[str, Any]:
    if isinstance(data, list):
        return [apply_schema(item, schema) for item in data]
    return {k: schema.get(k, lambda x: x)(data.get(k)) for k in schema}

def chain_process(data: Any, *steps: Callable) -> Any:
    return DataPipeline(data).transform(*steps).get()