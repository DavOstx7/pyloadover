from typing import List
from pyloadover.function import Function
from pyloadover.exceptions import (
    NamespaceMismatchError, SignatureExistsError, NoMatchingSignatureError, MultipleMatchingSignaturesError
)


class FunctionRegistry:
    def __init__(self, namespace: str, should_namespace_match: bool):
        self._namespace = namespace
        self._should_namespace_match = should_namespace_match
        self._functions: List[Function] = []

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def should_namespace_match(self) -> bool:
        return self._should_namespace_match

    def register(self, function: Function):
        if self._should_namespace_match and function.namespace != self.namespace:
            raise NamespaceMismatchError(f"Function '{function.namespace}' does not match registry '{self.namespace}'")

        if self.is_signature_exists(function):
            raise SignatureExistsError(
                f"Function signature {function.signature} already exists in registry '{self.namespace}'"
            )

        self._functions.append(function)

    def find_one_by_arguments(self, *args, **kwargs) -> Function:
        matches = self.find_by_arguments(*args, **kwargs)

        if len(matches) == 0:
            raise NoMatchingSignatureError(
                f"Provided arguments do not match any signature in registry '{self.namespace}'"
            )
        elif len(matches) > 1:
            raise MultipleMatchingSignaturesError(
                f"Provided arguments match multiple signatures in registry '{self.namespace}'"
            )
        return matches[0]

    def find_by_arguments(self, *args, **kwargs) -> List[Function]:
        return [f for f in self._functions if f.do_arguments_match_signature(*args, **kwargs)]

    def is_signature_exists(self, function: Function) -> bool:
        for f in self._functions:
            if f.signature == function.signature:
                return True
        return False
