import inspect
from typing import Callable, Any


class FunctionContext:
    def __init__(self, f: Callable[[...], Any]):
        self._callable = f
        self._signature = inspect.signature(f)

    @property
    def callable(self) -> Callable[[...], Any]:
        return self._callable

    @property
    def name(self) -> str:
        return self._callable.__name__

    @property
    def qualified_name(self) -> str:
        return self._callable.__qualname__

    @property
    def module(self) -> str:
        return self._callable.__module__

    @property
    def signature(self) -> inspect.Signature:
        return self._signature
