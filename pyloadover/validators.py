from abc import ABC, abstractmethod
from pyloadover.functions.model import Function
from pyloadover.groups.context import GroupContext
from pyloadover.exceptions import IdMismatchError, SignatureExistsError


class Validator(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


class GroupFunctionValidator(Validator):
    @abstractmethod
    def validate(self, group_context: GroupContext, function: Function):
        pass


class EqualIdsValidator(GroupFunctionValidator):
    def validate(self, group_context: GroupContext, function: Function):
        if function.id != group_context.id:
            raise IdMismatchError(f"Function '{function.id}' does not match group '{group_context.id}'")


class UniqueSignaturesValidator(GroupFunctionValidator):
    def validate(self, group_context: GroupContext, function: Function):
        if group_context.is_signature_exists(function.signature):
            raise SignatureExistsError(
                f"Function '{function.id}' signature {function.signature} already exists in group '{group_context.id}'"
            )
