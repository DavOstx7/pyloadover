import functools
from typing import Optional, List, Callable, Any
from pyloadover.config import CONFIG, ConfigReloadable
from pyloadover.functions import Function, FunctionContext
from pyloadover.groups.validators import GroupFunctionValidator, GroupContext
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


class Group(ConfigReloadable):
    def __init__(self, context: GroupContext, validators: Optional[List[GroupFunctionValidator]] = None):
        self._context = context
        self.validators = CONFIG["group_validators"] if validators is None else validators

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
        self.validators = CONFIG["group_validators"]

        for function in self.functions:
            function.reload_from_config()

    def clear(self):
        self.functions.clear()
        self.validators.clear()

    def register_function(self, function: Function):
        self.validate_function(function)

        self.functions.append(function)

    def validate_group(self):
        for function in self.functions:
            self.validate_function(function)

    def validate_function(self, function: Function):
        for validator in self.validators:
            validator.validate(self._context, function)

    def find_functions_by_arguments(self, *args, **kwargs) -> List[Function]:
        return [function for function in self.functions if function.do_arguments_match(*args, **kwargs)]

    def retrieve_function_by_arguments(self, *args, **kwargs) -> Function:
        matches = self.find_functions_by_arguments(*args, **kwargs)

        if not matches:
            raise NoMatchFoundError(
                f"Provided arguments do not match any signature in group '{self.id}'"
            )
        elif len(matches) > 1:
            raise MultipleMatchesFoundError(
                f"Provided arguments match multiple signatures in group '{self.id}'"
            )

        return matches[0]

    def call_function_by_arguments(self, *args, **kwargs) -> Any:
        retrieved_function = self.retrieve_function_by_arguments(*args, **kwargs)
        return retrieved_function(*args, **kwargs)

    def __call__(self, _object: Callable[[...], Any]) -> Callable[[...], Any]:
        function = Function(FunctionContext(_object))
        self.register_function(function)

        @functools.wraps(_object)
        def wrapper(*args, **kwargs):
            retrieved_function = self.retrieve_function_by_arguments(*args, **kwargs)
            return retrieved_function(*args, **kwargs)

        return wrapper
