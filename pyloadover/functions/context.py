import inspect
from typing import Callable, Any


class FunctionContext:
    def __init__(self, _object: Callable[[...], Any]):
        self._object = _object
        self._signature = inspect.signature(_object)

    @property
    def object(self) -> Callable[[...], Any]:
        return self._object

    @property
    def name(self) -> str:
        return self._object.__name__

    @property
    def qualified_name(self) -> str:
        return self._object.__qualname__

    @property
    def module(self) -> str:
        return self._object.__module__

    @property
    def signature(self) -> inspect.Signature:
        return self._signature
