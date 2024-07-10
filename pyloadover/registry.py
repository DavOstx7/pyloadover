from typing import List
from pyloadover.function import Function
from pyloadover.exceptions import (
    NameMismatchError, SignatureExistsError, NoMatchingSignatureError, MultipleMatchingSignaturesError
)


class FunctionRegistry:
    def __init__(self, name: str):
        self._name = name
        self._functions: List[Function] = []

    @property
    def name(self) -> str:
        return self._name

    def register(self, function: Function):
        if function.name != self.name:
            raise NameMismatchError(f"Function name '{function.name}' does not match registry name '{self.name}'")
        if self.is_signature_exists(function):
            raise SignatureExistsError(f"Function signature {function.signature} already exists in the registry")

        self._functions.append(function)

    def find_one_by_arguments(self, *args, **kwargs) -> Function:
        matches = self.find_by_arguments(*args, **kwargs)

        if len(matches) == 0:
            raise NoMatchingSignatureError(f"Provided arguments do not match any signature in registry '{self.name}'")
        elif len(matches) > 1:
            raise MultipleMatchingSignaturesError(
                f"Provided arguments match multiple signatures in registry '{self.name}'"
            )
        return matches[0]

    def find_by_arguments(self, *args, **kwargs) -> List[Function]:
        return [f for f in self._functions if f.do_arguments_match_signature(*args, **kwargs)]

    def is_signature_exists(self, function: Function) -> bool:
        for f in self._functions:
            if f.signature == function.signature:
                return True
        return False
