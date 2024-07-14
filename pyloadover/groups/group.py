from typing import Optional, List
from pyloadover.config import CONFIG, ConfigReloadable
from pyloadover.function import Function
from pyloadover.group.validators import GroupFunctionValidator, GroupContext
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


class Group(ConfigReloadable):
    def __init__(self, context: GroupContext, validators: Optional[List[GroupFunctionValidator]] = None):
        self.context = context
        self.validators = CONFIG["group_validators"] if validators is None else validators

    @property
    def id(self) -> str:
        return self.context.id

    @property
    def functions(self) -> List[Function]:
        return self.context.functions

    def reload_from_config(self):
        self.validators = CONFIG["group_validators"]

        for function in self.functions:
            function.reload_from_config()

    def clear(self):
        self.context.functions.clear()
        self.validators.clear()

    def register_function(self, function: Function):
        self.validate_function(function)

        self.functions.append(function)

    def validate_group(self):
        for function in self.functions:
            self.validate_function(function)

    def validate_function(self, function: Function):
        for validator in self.validators:
            validator.validate(self.context, function)

    def find_functions_by_arguments(self, *args, **kwargs) -> List[Function]:
        return [function for function in self.functions if function.do_arguments_match(*args, **kwargs)]

    def find_one_function_by_arguments(self, *args, **kwargs) -> Function:
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
