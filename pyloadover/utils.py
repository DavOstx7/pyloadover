import typeguard
from typing import Callable


def is_instance(value, annotation) -> bool:
    try:
        typeguard.check_type(value, annotation)
    except typeguard.TypeCheckError:
        return False
    else:
        return True


def get_namespace(function: Callable) -> str:
    return f"{function.__module__}.{function.__name__}"
