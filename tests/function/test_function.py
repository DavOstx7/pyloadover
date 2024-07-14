import pytest

from pyloadover.function import Function


@pytest.mark.parametrize("args,  kwargs", [
    ((1, "2"), {"c": True}),
    ((1, "2"), {})
])
def test_arguments_match_signature(args, kwargs, foo):
    assert Function(foo).do_arguments_match(*args, **kwargs)


@pytest.mark.parametrize("args,  kwargs", [
    ((), {}),
    ((1,), {}),
    ((1, 2), {"c": True}),
    ((1, "2"), {"c": 3}),
    ((1, "2"), {"c": True, "d": False}),
])
def test_arguments_not_match_signature(args, kwargs, foo):
    assert not Function(foo).do_arguments_match(*args, **kwargs)


def test_default_id(foo):
    assert Function(foo).id == "conftest.foo.<locals>.foo"


def test_not_fully_qualified_name_id(foo, use_name_as_function_id):
    assert Function(foo).id == "foo"
