# pyloadover

pyloadover is a python package which allows you to overload your functions in different ways.
It supports a lot of additional features, which you are more than welcome to discover yourself :)

## Installation

```shell
pip install pyloadover
```

## Basic Usage

```python
from pyloadover import overload


@overload
def function():
    return None


@overload
def function(x: int):
    return x ** 2


print("[1] Calling function():")
print(function())

print("[2] Calling function(5):")
print(function(5))

print("[3] Calling function(5, 25, 125):")
print(function(5, 25, 125))
```

```bash
[1] Calling function():
None
[2] Calling function(5):
25
[3] Calling function(5, 25, 125):
pyloadover.exceptions.NoMatchFoundError: Provided arguments [(5, 25, 125), {}] do not match any signature in group '__main__.function'
```

## Basic Config

```python
from pyloadover import overload, basic_config, FullyQualifiedNameIdGenerator, UniqueSignaturesValidator


@overload
def function():
    return None


basic_config(
    propagate=True,
    function_id_generator=FullyQualifiedNameIdGenerator(),
    group_function_validators=[UniqueSignaturesValidator()]
)


@overload
def function():
    return None
```

```bash
pyloadover.exceptions.SignatureExistsError: Function '__main__.function' signature () already exists in group '__main__.function'
```

__NOTE__: By default, the package is configured as follows:

```bash
basic_config(
    function_id_generator=FullyQualifiedNameIdGenerator(),
    group_function_validators=[EqualIdsValidator(), UniqueSignaturesValidator()]
)
```

## Groups

```python
import pyloadover
from pyloadover import get_group, pyoverload

function_group = get_group("__main__.function")


@function_group  # Method 1
def function(name: str):
    return f"Hello {name}!"


@pyoverload("__main__.function")  # Method 2
def function(first_name: str, last_name: str):
    return f"Hello {first_name}, your last name is {last_name}!"


@pyloadover.__main__.function  # Method 3
def function(first_name: str, middle_name: str, last_name: str):
    return f"Hello {first_name}, your middle name is {middle_name}, and your last name is {last_name}!"


print('[1] Calling function with params ("Foo"):')
print(function_group.call_function_by_arguments("Foo"))  # Method 1

print('[2] Calling function with params: ("Foo", "Bar"):')
print(function("Foo", "Bar"))  # Method 2

print('[3] Calling function with params: ("Foo", "IDK", "Bar"):')
print(function_group.find_single_function_by_arguments("Foo", "IDK", "Bar")("Foo", "IDK", "Bar"))  # Method 3
```

```bash
[1] Calling function with params ("Foo"):
Hello Foo!
[2] Calling function with params ("Foo", "Bar"):
Hello Foo, your last name is Bar!
[3] Calling function with params ("Foo", "IDK", "Bar"):
Hello Foo, your middle name is IDK, and your last name is Bar!
```

## Function ID Generators & Group Function Validators

These objects are used to fine-tune the package, and make it more solid/customizable.

### Function ID Generators

The function id generators, as their name indicates, are used to generate an id. This id, will be used to identify them,
and also belong them to a group with a matching id, unless specified otherwise.

* `FullyQualifiedNameIdGenerator`: Generates an ID which is composed out of the function's module and the function's
  qualified name.
* `NameIdGenerator`: Generates an ID which is composed out of the function's name.

### Group Function Validators

The group function validators, as their name indicates, are used to validate functions. These validators will be
activated upon a function registration, or a manual .validate() group call.

* `EqualIdsValidator`: Validates that the ID of the registered function matches the ID of the group it is registered to.
* `UniqueSignaturesValidator`: Validates that the signature of the registered function does not already exist in the
  group it is registered to.

__NOTE__: You could also create your own custom generators / validators!

```python
from pyloadover.functions import Function, FunctionContext, FunctionIdGenerator
from pyloadover.groups import GroupContext, GroupFunctionValidator


class CustomIdGenerator(FunctionIdGenerator):
    def generate_id(self, context: FunctionContext) -> str:
        pass


class CustomFunctionValidator(GroupFunctionValidator):
    def validate_function(self, group_context: GroupContext, function: Function):
        pass
```