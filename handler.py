import weakref
from collections import defaultdict
from typing import Callable, Any, Dict, List, Optional

class EventDispatcher:
    """Dynamic event pipeline with automatic stale reference cleanup."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Any]] = defaultdict(list)
        self._interceptors: List[Callable[[str, Any], Any]] = []

    def add_interceptor(self, fn: Callable[[str, Any], Any]) -> None:
        if fn not in self._interceptors:
            self._interceptors.append(fn)

    def subscribe(self, event: str, callback: Callable) -> None:
        if hasattr(callback, "__self__") and getattr(callback, "__self__", None) is not None:
            ref = weakref.WeakMethod(callback, lambda r: self._purge(event, r))
        else:
            ref = weakref.ref(callback, lambda r: self._purge(event, r))
        self._subscribers[event].append(ref)

    def _purge(self, event: str, dead_ref: weakref.ReferenceType) -> None:
        self._subscribers[event] = [r for r in self._subscribers[event] if r is not dead_ref]

    def dispatch(self, event: str, payload: Any = None) -> List[Any]:
        current_data = payload
        for interceptor in self._interceptors:
            current_data = interceptor(event, current_data)

        results = []
        for ref in list(self._subscribers.get(event, [])):
            func = ref()
            if func is not None:
                results.append(func(current_data))
        return results

    def compact(self) -> None:
        for event in list(self._subscribers.keys()):
            self._subscribers[event] = [r for r in self._subscribers[event] if r() is not None]
            if not self._subscribers[event]:
                del self._subscribers[event]
