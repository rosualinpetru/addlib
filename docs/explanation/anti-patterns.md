# Anti-patterns (what *not* to do)

For an audience with limited domain expertise, "here is the wrong way" is as
valuable as the how-to (roadmap Phase 6.2). For a real crypto library this page
would list parameter choices that silently destroy security. For `addlib` the
stakes are small, but the habit is the point.

## ❌ Assuming integer addition wraps

```python
add(2**63 - 1, 1)   # does NOT return -2**63; raises AdditionOverflowError
```

`add` is *checked*. If you genuinely want modular/wrapping arithmetic, do it
explicitly in Python (`(a + b) % 2**64`) — don't expect `addlib` to wrap.

## ❌ Comparing float results with `==`

```python
add_floats(0.1, 0.2) == 0.3      # False!  (0.30000000000000004)
```

Use a tolerance:

```python
from addlib.testing import approx_equal
approx_equal(add_floats(0.1, 0.2), 0.3)   # True
```

## ❌ Passing huge Python ints and expecting a result

```python
add(2**200, 1)   # raises — operands must fit in signed 64 bits
```

Use Python's built-in `int` for arbitrary precision. `addlib` is a 64-bit C core
and says so loudly rather than truncating.

## ❌ Reaching into private internals

```python
from addlib._add_cffi import lib   # private! may change without notice
```

The public API is `addlib.add`, `addlib.add_floats`, `addlib.c_version`,
`addlib.AdditionOverflowError`. Anything with a leading underscore
(`_add_cffi`, `_build_ffi`) is internal — see the
[design doc](design.md#6-public-api-surface-v0).

## ❌ Catching `Exception` to "handle overflow"

```python
try:
    result = add(a, b)
except Exception:   # too broad — hides bugs
    result = 0
```

Catch the specific `AdditionOverflowError` (or `OverflowError`), so real bugs
still surface.
