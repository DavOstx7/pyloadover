# pyloadover
Repository for developing and maintaining the code for pyloadover


## Installation

```shell
pip install pyloadover
```


### loadover

```python
from pyloadover import loadover


@loadover
def function():
    return None


@loadover
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
pyloadover.exceptions.NoMatchingSignatureError: Provided arguments do not match any signature in registry 'function'
```