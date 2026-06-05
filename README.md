# addlib

[![CI](https://github.com/rosualinpetru/addlib/actions/workflows/ci.yml/badge.svg)](https://github.com/rosualinpetru/addlib/actions/workflows/ci.yml)
[![Docs](https://github.com/rosualinpetru/addlib/actions/workflows/docs.yml/badge.svg)](https://github.com/rosualinpetru/addlib/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/rosualinpetru/addlib/branch/main/graph/badge.svg)](https://codecov.io/gh/rosualinpetru/addlib)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/rosualinpetru/addlib/badge)](https://securityscorecards.dev/viewer/?uri=github.com/rosualinpetru/addlib)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

> A small, complete example of a **Python library backed by a C core** through a
> CFFI ABI — and a **batteries-included template** for building, testing,
> securing, packaging, and releasing a native (C + Python) open-source library.

`addlib` adds two numbers. The functionality is trivial on purpose: the
**scaffolding is the point**. Clone it, rename it, replace `add` with your real
performance-critical C, and you start from a clean C/Python boundary, a serious
test strategy, cross-platform wheels, supply-chain security, and an automated
signed release.

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

## What this template gives you

| Area | What's included |
| --- | --- |
| **Architecture** | Clean C core (`libadd`) + thin CFFI binding + typed Python API; a documented C ABI as the contract |
| **Build** | Self-contained wheels (`cibuildwheel`) for Linux/macOS/Windows incl. Python 3.14; standalone CMake build for C consumers |
| **Testing** | Unit, property-based (Hypothesis), known-answer, adversarial/negative gates, ABI-contract tests; libFuzzer target; benchmarks |
| **Security** | ASan/UBSan + Valgrind, CodeQL, OpenSSF Scorecard, dependency review, private vuln reporting |
| **Release** | Tag-driven pipeline: SBOM + SLSA provenance + Sigstore signatures + PyPI Trusted Publishing + signed GitHub Release |
| **Docs** | MkDocs Material (Diátaxis), auto-generated API reference, runnable examples |
| **Project** | Apache-2.0, governance, DCO, Code of Conduct, issue/PR templates, RFC process, ADRs |

## Why it's built this way

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
make lint     # ruff, mypy, clang-format
make bench    # benchmarks
make fuzz     # libFuzzer (macOS: FUZZ_CC="$(brew --prefix llvm)/bin/clang")
make docs     # build the documentation site
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions are under the
[DCO](https://developercertificate.org/) (`git commit -s`).

## Documentation

- **Tutorials / how-to / reference / explanation**: see [`docs/`](docs/) (Diátaxis).
- **Design document**: [docs/explanation/design.md](docs/explanation/design.md).
- **Security model & disclosure**: [SECURITY.md](SECURITY.md),
  [docs/explanation/security-model.md](docs/explanation/security-model.md).
- **Project tour**: [docs/ROADMAP.md](docs/ROADMAP.md).

## Security

Found a vulnerability? **Do not** open a public issue — see
[SECURITY.md](SECURITY.md). (For an addition library the attack surface is small;
the *process* is the point.)

## License

[Apache-2.0](LICENSE) © Alin-Petru Roșu. See [NOTICE](NOTICE).
