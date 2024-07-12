import inspect
from typing import List
from pyloadover.function import Function
from pyloadover.exceptions import (
    MismatchedIdError, DuplicatedSignatureError, NoMatchFoundError, MultipleMatchesFoundError
)


class Group:
    def __init__(self, _id: str, allow_mismatched_ids: bool = False, allow_duplicated_signatures: bool = False):
        self._id = _id
        self._functions: List[Function] = []
        self.allow_mismatched_names = allow_mismatched_ids
        self.allow_duplicated_signatures = allow_duplicated_signatures

    @property
    def id(self) -> str:
        return self._id

    @property
    def functions(self) -> List[Function]:
        # Shallow Copy
        return self._functions.copy()

    def clear(self):
        self._functions.clear()

    def register(self, function: Function):
        if not self.allow_mismatched_names and function.id != self.id:
            raise MismatchedIdError(
                f"Function '{function.id}' does not match group '{self.id}'"
            )

        if not self.allow_duplicated_signatures and self.is_signature_exists(function.signature):
            raise DuplicatedSignatureError(
                f"Function signature {function.signature} already exists in group '{self.id}'"
            )

        self._functions.append(function)

    def find_by_arguments(self, *args, **kwargs) -> List[Function]:
        return [function for function in self._functions if function.do_arguments_match(*args, **kwargs)]

    def find_one_by_arguments(self, *args, **kwargs) -> Function:
        matches = self.find_by_arguments(*args, **kwargs)

        if len(matches) == 0:
            raise NoMatchFoundError(
                f"Provided arguments do not match any signature in group '{self.id}'"
            )
        elif len(matches) > 1:
            raise MultipleMatchesFoundError(
                f"Provided arguments match multiple signatures in group '{self.id}'"
            )

        return matches[0]

    def is_signature_exists(self, signature: inspect.Signature) -> bool:
        for function in self._functions:
            if function.signature == signature:
                return True
        return False
