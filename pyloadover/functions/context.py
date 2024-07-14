import inspect
from typing import Callable


class FunctionContext:
    def __init__(self, _object: Callable):
        self._object = _object
        self._signature = inspect.signature(_object)

    @property
    def object(self) -> Callable:
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
