"""Dynamic pipeline event handler with flexible callback registration."""

import functools
import inspect
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
)

T = TypeVar("T")
HandlerFunc = Callable[..., Any]


class DynamicHandler:
    """A flexible task handler supporting topic-based dynamic execution pipelines.

    Allows subscribing functions to specific topics and executing them sequentially
    with positional or dynamic keyword arguments.
    """

    def __init__(self, name: str = "default_handler") -> None:
        self.name: str = name
        self._registry: Dict[str, List[HandlerFunc]] = {}
        self._history: List[Tuple[str, Any]] = []

    def register(self, topic: str) -> Callable[[HandlerFunc], HandlerFunc]:
        """Decorator to register a callable under a specific event topic.

        Args:
            topic: String identifier representing the event category.

        Returns:
            A decorator function that registers and returns the original function.
        """
        def decorator(func: HandlerFunc) -> HandlerFunc:
            if topic not in self._registry:
                self._registry[topic] = []
            self._registry[topic].append(func)

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def dispatch(self, topic: str, *args: Any, **kwargs: Any) -> List[Any]:
        """Execute all registered callbacks for a given topic.

        Args:
            topic: Event topic to trigger.
            *args: Positional arguments passed to handlers.
            **kwargs: Keyword arguments passed to handlers.

        Returns:
            List of return values produced by each executed handler.
        """
        results: List[Any] = []
        handlers = self._registry.get(topic, [])
        for handler in handlers:
            sig = inspect.signature(handler)
            if len(sig.parameters) == 0:
                res = handler()
            else:
                res = handler(*args, **kwargs)
            results.append(res)
            self._history.append((topic, res))
        return results

    def get_history(self, topic: Optional[str] = None) -> List[Tuple[str, Any]]:
        """Retrieve historical execution results.

        Args:
            topic: Optional topic filter. If None, returns all logged history.

        Returns:
            List of (topic, output_result) tuples matching the filter.
        """
        if topic is None:
            return list(self._history)
        return [item for item in self._history if item[0] == topic]
