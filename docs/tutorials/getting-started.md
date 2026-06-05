# Getting started

Your first addition in five minutes. This is a *learning-oriented* tutorial —
follow it top to bottom.

## 1. Install

```bash
pip install addlib
```

No C compiler is needed: the wheel already contains the compiled `libadd` core.

## 2. Add two integers

```python
from addlib import add

print(add(2, 3))      # 5
print(add(-10, 4))    # -6
```

`add` works on signed 64-bit integers and is computed in C. It is *checked*: if
the result would not fit in 64 bits, it raises rather than wrapping.

```python
from addlib import add, AdditionOverflowError

try:
    add(2**63 - 1, 1)
except AdditionOverflowError as exc:
    print("too big:", exc)
```

## 3. Add two floats

```python
from addlib import add_floats

print(add_floats(0.5, 0.25))   # 0.75
print(add_floats(0.1, 0.2))    # 0.30000000000000004  (IEEE-754 rounding)
```

Float results are *approximate*. Compare them with a tolerance, never with `==`:

```python
from addlib.testing import approx_equal
assert approx_equal(add_floats(0.1, 0.2), 0.3)
```

## 4. Check the versions line up

```python
import addlib
print(addlib.__version__, addlib.c_version())   # 0.1.1 0.1.1
```

The Python package and the native core report the same version — a test enforces
this so they can never drift.

## Next steps

- [Handle overflow safely](../how-to/handling-overflow.md)
- [Use `libadd` directly from C](../how-to/use-libadd-from-c.md)
- [Why the API is shaped this way](../explanation/design.md)
