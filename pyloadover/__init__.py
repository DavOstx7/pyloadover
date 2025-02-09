from typing import Callable, Any
from .functions import Function, FunctionIdGenerator, NameIdGenerator, FullyQualifiedNameIdGenerator
from .groups import Group, GroupFunctionValidator, EqualIdsValidator, UniqueSignaturesValidator
from .pyloadover import overloader, overload, get_or_create_group, configure

configure(
    function_id_generator=FullyQualifiedNameIdGenerator(),
    group_function_validators=[EqualIdsValidator(), UniqueSignaturesValidator()]
)


class DynamicOverloadBuilder:
    def __init__(self, name: str):
        self.name = name

    def __getattr__(self, item: str) -> "DynamicOverloadBuilder":
        self.name = f"{self.name}.{item}"
        return self

    def __call__(self, f: Callable[[...], Any]) -> Callable[[...], Any]:
        return overloader(self.name)(f)


def __getattr__(item: str) -> DynamicOverloadBuilder:
    return DynamicOverloadBuilder(item)
