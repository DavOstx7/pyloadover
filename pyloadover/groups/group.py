import functools
from typing import Optional, List, Callable, Any
from pyloadover.config import CONFIG, ConfigReloadable
from pyloadover.functions import Function
from pyloadover.groups.function_validators import GroupFunctionValidator, GroupContext
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


class Group(ConfigReloadable):
    def __init__(self, context: GroupContext, validators: Optional[List[GroupFunctionValidator]] = None):
        self._context = context
        self.validators = CONFIG["group_function_validators"] if validators is None else validators

    @classmethod
    def from_group_id(cls, group_id: str, validators: Optional[List[GroupFunctionValidator]] = None):
        return cls(GroupContext(group_id), validators=validators)

    @property
    def context(self) -> GroupContext:
        return self._context

    @property
    def id(self) -> str:
        return self._context.id

    @property
    def functions(self) -> List[Function]:
        return self._context.functions

    def reload_from_config(self):
        self.validators = CONFIG["group_function_validators"]

        for function in self.functions:
            function.reload_from_config()

    def clear(self):
        self.functions.clear()
        self.validators.clear()

    def register_function(self, function: Function):
        self.validate_function(function)

        self.functions.append(function)

    def validate(self):
        for function in self.functions:
            self.validate_function(function)

    def validate_function(self, function: Function):
        for validator in self.validators:
            validator.validate_function(self._context, function)

    def retrieve_matching_functions(self, *args, **kwargs) -> List[Function]:
        return [function for function in self.functions if function.do_arguments_match_signature(*args, **kwargs)]

    def retrieve_single_matching_function(self, *args, **kwargs) -> Function:
        matches = self.retrieve_matching_functions(*args, **kwargs)

        if not matches:
            raise NoMatchFoundError(
                f"Provided arguments [{args}, {kwargs}] do not match any signature in group '{self.id}'"
            )
        elif len(matches) > 1:
            raise MultipleMatchesFoundError(
                f"Provided arguments [{args}, {kwargs}] match multiple signatures in group '{self.id}'"
            )

        return matches[0]

    def call_matching_function(self, *args, **kwargs) -> Any:
        retrieved_function = self.retrieve_single_matching_function(*args, **kwargs)
        return retrieved_function(*args, **kwargs)

    def wraps(self, function: Function) -> Callable[[...], Any]:
        self.register_function(function)

        @functools.wraps(function.object)
        def wrapper(*args, **kwargs):
            return self.call_matching_function(*args, **kwargs)

        return wrapper

    def __call__(self, f: Callable[[...], Any]) -> Callable[[...], Any]:
        function = Function.from_callable(f)
        return self.wraps(function)
