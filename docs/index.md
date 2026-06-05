# addlib

**Checked integer & float addition with a C core, exposed to Python via a CFFI ABI.**

`addlib` adds two numbers — on purpose. It is a worked, end-to-end example of the
VERIFHE open-source library roadmap: a C performance core (`libadd`) bound to a
Python API (`addlib`) through a CFFI ABI, taken through every phase of building a
real, security-critical open-source library.

The shape is faithful; the payload is trivial. Read it in an afternoon, lift the
scaffolding.

## 30 seconds

```python
from addlib import add, add_floats

add(2, 3)              # 5  — computed in C, overflow-checked
add_floats(0.1, 0.2)   # 0.30000000000000004
```

```bash
pip install addlib     # self-contained wheel, no toolchain needed
```

## Where to go next

<div class="grid cards" markdown>

- **Tutorials** — learning-oriented. Start at
  [Getting started](tutorials/getting-started.md).
- **How-to guides** — task-oriented. E.g.
  [Handle overflow safely](how-to/handling-overflow.md),
  [Use `libadd` from C](how-to/use-libadd-from-c.md).
- **Reference** — the exact API: [Python](reference/python-api.md) ·
  [C](reference/c-api.md).
- **Explanation** — the *why*: [design](explanation/design.md),
  [security model](explanation/security-model.md),
  [testing](explanation/testing.md).

</div>

## Safety in one line

`add` never wraps silently: an out-of-range result raises
`AdditionOverflowError`. See the [anti-patterns](explanation/anti-patterns.md)
page for the misuse this prevents.
