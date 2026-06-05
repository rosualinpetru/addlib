# Project tour & roadmap

`addlib` is a template for a native (C + Python) open-source library. This page
maps the **lifecycle areas** of such a project to the concrete files here, so you
can see where each concern lives — and what's planned next.

## What's included

| Area | In `addlib` |
| --- | --- |
| **Foundations** | [`LICENSE`](https://github.com/rosualinpetru/addlib/blob/main/LICENSE) (Apache-2.0), [`NOTICE`](https://github.com/rosualinpetru/addlib/blob/main/NOTICE), [`GOVERNANCE.md`](https://github.com/rosualinpetru/addlib/blob/main/GOVERNANCE.md), [`SECURITY.md`](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md), [`CODE_OF_CONDUCT.md`](https://github.com/rosualinpetru/addlib/blob/main/CODE_OF_CONDUCT.md), [`CONTRIBUTING.md`](https://github.com/rosualinpetru/addlib/blob/main/CONTRIBUTING.md) (DCO) |
| **Architecture** | `c/` core + `add.h` ABI, CFFI binding, `addlib` API, [design doc](explanation/design.md), [ADRs](adr/README.md) |
| **Build & CI** | `pyproject.toml`/`setup.py`, `cibuildwheel`, `Makefile`, devcontainer, `ci.yml`/`wheels.yml`, Dependabot |
| **Testing** | unit/property/known-answer/negative/ABI tests, libFuzzer target with a 128-bit oracle, `pytest-benchmark`, nightly Valgrind |
| **Security** | [security model](explanation/security-model.md), [disclosure runbook](explanation/disclosure-runbook.md), CodeQL, OpenSSF Scorecard, dependency review |
| **Releases** | [versioning](explanation/versioning.md), [`CHANGELOG.md`](changelog.md), `release.yaml` (SBOM + provenance + Sigstore + Trusted Publishing) |
| **Docs & site** | this MkDocs Material site, `README.md`, `CITATION.cff`, runnable examples |
| **Community** | issue/PR templates, this page, [RFC template](https://github.com/rosualinpetru/addlib/tree/main/docs/rfcs) |
| **Maintenance** | ADRs + design doc as release-blocking artifacts, [`MAINTAINERS.md`](https://github.com/rosualinpetru/addlib/blob/main/MAINTAINERS.md) |

## A principle worth keeping

Testing and security tooling belong at the **front** of the timeline, not the
end. In `addlib` the test suite, fuzzer, sanitizers, and supply-chain workflows
existed before there was more than one function — for a correctness-critical
library, the tests *are* the argument.

## Forward roadmap (illustrative)

- **0.2** — a saturating/wrapping `add` variant (seeds the *experimental* tier),
  behind a clearly-marked import.
- **0.3** — vectorized addition over buffers (NumPy protocol); may justify a
  second published Python artifact.
- **0.x → 1.0** — stabilize the API; reach `1.0` when the public surface can be
  promised, per [versioning](explanation/versioning.md).
- **C library** — publish `libadd` to conda-forge / vcpkg if and when C
  consumers ask (demand-driven).

Bigger or breaking changes go through the lightweight
[RFC process](https://github.com/rosualinpetru/addlib/tree/main/docs/rfcs).
