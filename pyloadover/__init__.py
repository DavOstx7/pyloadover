from typing import Callable
from .pyloadover import pyloadover, loadover
from .config import basic_config


class _DynamicGroupLoader:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        self.name = f"{self.name}.{item}"
        return self

    def __call__(self, f: Callable):
        return pyloadover(self.name)(f)


def __getattr__(group: str):
    return _DynamicGroupLoader(group)
