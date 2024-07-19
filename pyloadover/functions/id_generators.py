from abc import ABC, abstractmethod
from pyloadover.functions.context import FunctionContext


class FunctionIdGenerator(ABC):
    @abstractmethod
    def generate_id(self, context: FunctionContext) -> str:
        pass


class FullyQualifiedNameIdGenerator(FunctionIdGenerator):
    def generate_id(self, context: FunctionContext):
        return f"{context.module}.{context.qualified_name}"


class NameIdGenerator(FunctionIdGenerator):
    def generate_id(self, context: FunctionContext):
        return context.name
