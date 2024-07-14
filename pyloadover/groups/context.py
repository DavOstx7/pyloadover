import inspect
from typing import Optional, List
from pyloadover.functions import Function


class GroupContext:
    def __init__(self, _id: str, functions: Optional[List[Function]] = None):
        self._id = _id
        self._functions = [] if functions is None else functions

    @property
    def id(self) -> str:
        return self._id

    @property
    def functions(self) -> List[Function]:
        return self._functions

    def is_signature_exists(self, signature: inspect.Signature) -> bool:
        for function in self._functions:
            if function.signature == signature:
                return True
        return False
