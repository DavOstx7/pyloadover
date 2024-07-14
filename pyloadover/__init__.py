from typing import Callable
from .functions import Function, FunctionIdGenerator, NameIdGenerator, FullyQualifiedNameIdGenerator
from .groups import Group, GroupFunctionValidator, EqualIdsValidator, UniqueSignaturesValidator
from .pyloadover import pyoverload, loadover, basic_config

basic_config(
    function_id_generator=FullyQualifiedNameIdGenerator(),
    group_validators=[EqualIdsValidator(), UniqueSignaturesValidator()]
)


class DynamicGroupLoader:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        self.name = f"{self.name}.{item}"
        return self

    def __call__(self, f: Callable):
        return pyoverload(self.name)(f)


def __getattr__(item: str):
    return DynamicGroupLoader(item)
