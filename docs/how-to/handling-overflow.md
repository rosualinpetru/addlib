# How to handle overflow safely

`add` operates on signed 64-bit integers. When the true sum is outside
`[-2**63, 2**63 - 1]`, it raises `AdditionOverflowError` instead of returning a
wrong (wrapped) value.

## Catch it

```python
from addlib import add, AdditionOverflowError

def safe_add(a: int, b: int) -> int | None:
    try:
        return add(a, b)
    except AdditionOverflowError:
        return None
```

## It is an `OverflowError`

`AdditionOverflowError` subclasses the built-in `OverflowError`, so existing
handlers keep working:

```python
try:
    add(2**63 - 1, 1)
except OverflowError:
    ...  # also catches AdditionOverflowError
```

## Out-of-range inputs raise too

You cannot sneak an out-of-range operand in — it is rejected before the C call:

```python
add(2**63, 0)   # raises AdditionOverflowError: a is outside the signed 64-bit range
```

## Need unbounded integers?

Use Python's built-in `int` — it is arbitrary precision. `addlib` deliberately
bounds to 64 bits (that is what the C core is) and refuses to pretend otherwise.

```python
a, b = 2**200, 2**200
a + b           # fine in pure Python
add(a, b)       # raises — by design
```
