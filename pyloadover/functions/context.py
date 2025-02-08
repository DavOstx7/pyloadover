import inspect
from typing import Callable, Any, Optional
from pyloadover.utils import get_underlying_callable


class FunctionContext:
    def __init__(self, f: Callable[[...], Any]):
        underlying_callable = get_underlying_callable(f)
        signature = inspect.signature(underlying_callable) if underlying_callable else inspect.signature(f)

        self._callable = f
        self._underlying_callable = underlying_callable
        self._signature = signature

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
    def underlying_callable(self) -> Optional[Callable[[...], Any]]:
        return self._underlying_callable

    @property
    def signature(self) -> inspect.Signature:
        return self._signature
