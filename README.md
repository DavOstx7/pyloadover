# pyloadover

**Function Overloading Made Easy in Python**

`pyloadover` is a Python package that enables **function overloading** in Python. It allows you to define multiple
implementations of a function with different signatures and automatically selects the appropriate one based on the
arguments provided. Additionally, it offers advanced features like **custom ID generation**, **validation**, and **group
management** for overloaded functions.

---

## Installation

Install pyloadover using pip:

```bash
pip install pyloadover
```

__NOTE__: `pyloadover` requires Python3.8 or higher.

---

## Quick Start

### Basic Overloading

Function overloading allows you to define multiple implementations of a function with different signatures.
`pyloadover` automatically selects the appropriate implementation based on the arguments provided.

Here’s how you can use `pyloadover` to overload functions:

```python
from pyloadover import overload


@overload
def greet():
    return "Hello, World!"


@overload
def greet(name: str):
    return f"Hello, {name}!"


@overload
def greet(first_name: str, last_name: str):
    return f"Hello, {first_name} {last_name}!"


# Calling the overloaded functions
print(greet())  # Output: Hello, World!
print(greet("Alice"))  # Output: Hello, Alice!
print(greet("Alice", "Smith"))  # Output: Hello, Alice Smith!
```

If no matching function is found, a `NoMatchingSignatureError` is raised:

```python
print(greet(1, 2, 3))  # Raises: NoMatchingSignatureError
```

--- 

## Configuration

You can configure `pyloadover` using the `configure` function. For example,
you can enforce unique function signatures and customize how function IDs are generated:

- `propagate`: Applies the configuration to all existing and future groups.
- `function_id_generator`: Determines how function IDs are generated (e.g., using fully qualified names).
  When no group is explicitly specified,
  these IDs are used to automatically assign functions to their respective groups.
- `group_function_validators`: Ensures functions meet specific criteria when added to a group (e.g., unique signatures).

```python
from pyloadover import overload, configure, QualifiedNameIdGenerator, SignatureUniquenessValidator


@overload
def greet():
    return "Hello, World!"


# Configure pyloadover
configure(
    propagate=True,  # Propagate configuration to all groups
    function_id_generator=QualifiedNameIdGenerator(),  # Use fully qualified names as IDs
    group_function_validators=[SignatureUniquenessValidator()]  # Enforce unique signatures
)


# Attempting to register a duplicate signature will raise an error
@overload
def greet():
    return "Hello again!"
```

```bash
SignatureExistsError: Function 'main.greet' with signature () already exists in group 'main.greet'
```

--- 

## Function Groups

pyloadover allows you to organize overloaded functions into groups. A group is a collection of functions that share the
same name but have different signatures.

### Creating and Using Groups

You can create and manage groups in three ways:

#### Method 1: Using `get_or_create_group`

```python
from pyloadover import get_or_create_group

greet_group = get_or_create_group("greet")


@greet_group
def greet(name: str):
    return f"Hello, {name}!"
```

#### Method 2: Using `overloader`

```python
from pyloadover import overloader


@overloader("greet")
def greet(first_name: str, last_name: str):
    return f"Hello, {first_name} {last_name}!"
```

#### Method 3: Using the Dynamic Overload Builder

```python
import pyloadover


@pyloadover.greet
def greet(first_name: str, middle_name: str, last_name: str):
    return f"Hello, {first_name} {middle_name} {last_name}!"
```

### Calling Functions in a Group

You can call functions in a group using their arguments:

```python
print(greet("Alice"))  # Output: Hello, Alice!
print(greet("Alice", "Smith"))  # Output: Hello, Alice Smith!
print(greet("Alice", "Marie", "Smith"))  # Output: Hello, Alice Marie Smith!
```

You can also call functions by using their group:

```python
greet_group.find_single_function_by_arguments("Alice")("Alice")  # Output: Hello, Alice!
greet_group.call_function_by_arguments("Alice", "Smith")  # Output: Hello, Alice Smith!
```

---

## Advanced Features

### Custom ID Generators

ID generators determine how functions are identified and grouped.
`pyloadover` provides two built-in generators:

* `QualifiedNameIdGenerator`: Uses the function’s module and qualified name as the ID.
* `NameIdGenerator`: Uses the function’s name as the ID.

You can also create custom ID generators:

```python
from pyloadover import FunctionIdGenerator, FunctionContext


class CustomIdGenerator(FunctionIdGenerator):
    def generate_id(self, context: FunctionContext) -> str:
        return f"custom_{context.function.name}"
```

### Custom Validators

Validators ensure that functions meet specific criteria when added to a group.
`pyloadover` provides two built-in validators:

* `EqualIdsValidator`: Ensures the function’s ID matches the group’s ID.
* `SignatureUniquenessValidator`: Ensures no two functions in a group have the same signature.

You can create custom validators:

```python
from pyloadover import GroupFunctionValidator, GroupContext, Function


class CustomValidator(GroupFunctionValidator):
    def validate_function(self, group_context: GroupContext, function: Function):
        if "admin" in function.context.name:
            raise ValueError("Admin functions are not allowed!")
```

---

## Default Configuration

By default, pyloadover is configured as follows:

```python
configure(
    function_id_generator=QualifiedNameIdGenerator(),
    group_function_validators=[EqualIdsValidator(), SignatureUniquenessValidator()]
)
```

---

## Contributing

If you’d like to contribute to `pyloadover`, feel free to open an issue or
submit a pull request on [GitHub](https://github.com/DavOstx7/pyloadover).

---

## License

pyloadover is licensed under the MIT License. See [LICENSE](LICENSE) for more details.