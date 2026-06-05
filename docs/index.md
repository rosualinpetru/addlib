# addlib

**A Python library backed by a C core through a CFFI ABI — and a template for
building, testing, securing, packaging, and releasing a native (C + Python)
open-source library.**

`addlib` adds two numbers. The functionality is trivial on purpose; the
scaffolding around it is what's worth copying: a clean C/Python boundary, a real
test strategy, cross-platform wheels, supply-chain security, and an automated
signed release.

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
