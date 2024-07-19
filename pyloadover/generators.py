from abc import ABC, abstractmethod
from typing import Any
from pyloadover.functions.context import FunctionContext


class Generator(ABC):
    @abstractmethod
    def generate(self, *args, **kwargs) -> Any:
        pass


class FunctionIdGenerator(Generator):
    @abstractmethod
    def generate(self, context: FunctionContext) -> str:
        pass


class FullyQualifiedNameIdGenerator(FunctionIdGenerator):
    def generate(self, context: FunctionContext):
        return f"{context.module}.{context.qualified_name}"


class NameIdGenerator(FunctionIdGenerator):
    def generate(self, context: FunctionContext):
        return context.name
