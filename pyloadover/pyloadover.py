from typing import Optional, List, Callable, Any
from pyloadover.functions import Function, FunctionIdGenerator
from pyloadover.groups import Group, GroupFunctionValidator
from pyloadover.manager import manager
from pyloadover.config import update_config_if_value_exists


def configure(
        propagate: bool = False,
        *,
        function_id_generator: Optional[FunctionIdGenerator] = None,
        group_function_validators: Optional[List[GroupFunctionValidator]] = None
):
    update_config_if_value_exists("function_id_generator", function_id_generator)
    update_config_if_value_exists("group_function_validators", group_function_validators)

    if propagate:
        manager.reload_from_config()


def get_or_create_group(group_id: str) -> Group:
    return manager.get_or_create_group(group_id)


def resolve_group_id(group_id: Optional[str], function: Function) -> str:
    return function.id if group_id is None else group_id


# TODO: better type hinting for decorators/wrappers
def overloader(group_id: Optional[str] = None) -> Callable[[...], Any]:
    def decorator(f: Callable[[...], Any]) -> Callable[[...], Any]:
        function = Function.from_callable(f)
        resolved_group_id = resolve_group_id(group_id, function)
        group = manager.get_or_create_group(resolved_group_id)
        return group.wraps(function)

    return decorator


overload = overloader()
