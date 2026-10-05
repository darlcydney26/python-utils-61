import sys
from typing import Any, Generator, Iterable, Dict, List, get_type_hints

# Python 3.9+ compatibility fallback
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    class AnnotatedMeta(type):
        def __getitem__(cls, params):
            return params[0]
    class Annotated(metaclass=AnnotatedMeta):
        pass

def min_length(limit: int):
    return lambda v: v is not None and len(str(v)) >= limit

def matches_format(prefix: str):
    return lambda v: v is not None and str(v).startswith(prefix)

class Transaction:
    sender: Annotated[str, min_length(3), matches_format("usr_")]
    amount: Annotated[int, lambda v: isinstance(v, int) and v > 0]

class ProcessingLoop:
    """
    Stream processor filtering input packets through inline schema-annotated rules.
    """
    def __init__(self, schema_cls: type):
        self.schema_cls = schema_cls
        self.validators = self._build_validators()

    def _build_validators(self) -> Dict[str, List[Any]]:
        validators = {}
        for field_name, type_hint in get_type_hints(self.schema_cls, include_extras=True).items():
            checks = []
            if hasattr(type_hint, "__metadata__"):
                for metadata in type_hint.__metadata__:
                    if callable(metadata):
                        checks.append(metadata)
            validators[field_name] = checks
        return validators

    def process(self, stream: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """
        Main loop validating data elements dynamically and discarding malformed payloads.
        """
        for index, raw_item in enumerate(stream):
            if not isinstance(raw_item, dict):
                continue

            try:
                valid = True
                for field, checks in self.validators.items():
                    value = raw_item.get(field)
                    if not all(check(value) for check in checks):
                        valid = False
                        break

                if valid:
                    # Return safe, shallow copy of the validated transaction
                    yield {**raw_item, "_id": index}
            except (AttributeError, KeyError, ValueError):
                # Absorb unexpected transient operational errors