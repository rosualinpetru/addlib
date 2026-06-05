# addlib

> **Checked integer & float addition with a C core, exposed to Python via a CFFI ABI.**

`addlib` adds two numbers. That is all it does — on purpose.

It is a **worked, end-to-end example** of the
VERIFHE open-source library roadmap: a C
performance core (`libadd`) bound to a Python API (`addlib`) through a CFFI ABI,
carried through every phase of building a real open-source, security-critical
library — licensing, governance, CI/CD, a serious test strategy, supply-chain
security, automated signed releases, documentation, community, and maintenance.

Wherever the real VERIFHE library would have RNS arithmetic, CKKS, PIOPs and a
SNARK, `addlib` has `add_i64` and `add_f64`. **The shape is faithful; the payload
is trivial**, so you can read the whole thing in an afternoon and lift the
scaffolding.

## Install

```bash
pip install addlib          # self-contained wheel; no C toolchain required
```

## Quickstart (Python)

```python
from addlib import add, add_floats, AdditionOverflowError

add(2, 3)                 # -> 5   (computed in C, overflow-checked)
add_floats(0.1, 0.2)      # -> 0.30000000000000004  (IEEE-754)

try:
    add(2**63 - 1, 1)     # would overflow signed 64-bit
except AdditionOverflowError as exc:
    print("rejected:", exc)   # never wraps silently
```

## Quickstart (C — the standalone `libadd`)

```c
#include <add/add.h>
#include <stdio.h>

int main(void) {
    int64_t out;
    if (add_i64(20, 22, &out) == ADD_OK) {
        printf("%lld\n", (long long)out);  // 42
    }
}
```

```bash
cmake -S . -B build && cmake --build build   # builds libadd + CMake/pkg-config
```

## Why it's built the way it is

| Decision | Choice | Rationale |
| --- | --- | --- |
| License | Apache-2.0 | Patent grant; industry-friendly ([ADR-0001](docs/adr/0001-license-apache-2.0.md)) |
| Binding | CFFI (API mode) | Best fit for a pure-C core ([ADR-0002](docs/adr/0002-cffi-binding.md)) |
| Artifacts | Monorepo → `libadd` (C) + `addlib` (Python) | Multi-artifact future, no day-one cost ([ADR-0003](docs/adr/0003-monorepo-two-artifacts.md)) |
| Build | setuptools+CFFI (wheel), CMake (C lib) | CFFI owns its extension ([ADR-0004](docs/adr/0004-build-backend.md)) |

## Repository layout

```
addlib/
├── c/                     # libadd: the C performance core (CMake, pkg-config)
│   ├── include/add/add.h  # the C-ABI contract
│   ├── src/add.c          # the implementation
│   ├── tests/  fuzz/  bench/
├── python/
│   ├── src/addlib/        # the Python package + CFFI build script
│   └── tests/             # unit, property, KAT, negative, ABI-contract
├── docs/                  # Diátaxis docs + ADRs + design doc
├── examples/   benchmarks/
└── .github/workflows/     # CI, wheels, nightly, release, CodeQL, scorecard
```

## Develop

```bash
make dev      # venv + dev deps + build the extension
make test     # C tests (CTest) + Python tests (pytest)
make lint     # ruff, mypy, clang-format/-tidy
make bench    # benchmarks
make docs     # build the documentation site
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions are under the
[DCO](https://developercertificate.org/) (`git commit -s`).

## Documentation

- **Tutorials / how-to / reference / explanation**: see [`docs/`](docs/) (Diátaxis).
- **Design document**: [docs/explanation/design.md](docs/explanation/design.md).
- **Security model & disclosure**: [SECURITY.md](SECURITY.md),
  [docs/explanation/security-model.md](docs/explanation/security-model.md).
- **How the phases map to a timeline**: [docs/ROADMAP.md](docs/ROADMAP.md).

## Security

Found a vulnerability? **Do not** open a public issue — see
[SECURITY.md](SECURITY.md). (For an addition library the attack surface is small;
the *process* is the point.)

## License

[Apache-2.0](LICENSE) © Alin-Petru Roșu. See [NOTICE](NOTICE).
