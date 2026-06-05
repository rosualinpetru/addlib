# Roadmap mapping

`addlib` is a worked example of the
VERIFHE library roadmap (the open-source-library design document this repo
accompanies). This page maps each roadmap **phase** to the concrete artifacts in this
repository, and sketches a forward roadmap.

## What each phase produced

| Phase | In the roadmap | In `addlib` |
| --- | --- | --- |
| **0 — Foundations** | License, governance, security intake, CoC, contribution basis | [`LICENSE`](https://github.com/rosualinpetru/addlib/blob/main/LICENSE) (Apache-2.0), [`NOTICE`](https://github.com/rosualinpetru/addlib/blob/main/NOTICE), [`GOVERNANCE.md`](https://github.com/rosualinpetru/addlib/blob/main/GOVERNANCE.md), [`SECURITY.md`](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md), [`CODE_OF_CONDUCT.md`](https://github.com/rosualinpetru/addlib/blob/main/CODE_OF_CONDUCT.md), [`CONTRIBUTING.md`](https://github.com/rosualinpetru/addlib/blob/main/CONTRIBUTING.md) (DCO) |
| **1 — Architecture** | C/Python boundary, modules, artifact decision, design doc | `c/` core + `add.h` ABI, CFFI binding, `addlib` API, [design doc](explanation/design.md), [ADRs](adr/README.md) |
| **2 — Infra & CI/CD** | CI, cross-platform wheels, dev env, SBOM | `pyproject.toml`/`setup.py`, `cibuildwheel`, `Makefile`, devcontainer, `ci.yml`/`wheels.yml`, Dependabot |
| **3 — Testing** | Pyramid, KATs, negative tests, fuzzing, benchmarks | unit/property/KAT/negative/ABI tests, libFuzzer target with a 128-bit oracle, `pytest-benchmark`, nightly Valgrind |
| **4 — Security** | Secure-by-construction, supply chain, disclosure, audit | [security model](explanation/security-model.md), [disclosure runbook](explanation/disclosure-runbook.md), CodeQL, OpenSSF Scorecard, dependency review |
| **5 — Releases** | SemVer, automated signed releases, channels | [versioning](explanation/versioning.md), [`CHANGELOG.md`](changelog.md), `release.yml` (SBOM + provenance + Sigstore + Trusted Publishing) |
| **6 — Docs & site** | Diátaxis, docs-as-code, website | this MkDocs Material site, `README.md`, `CITATION.cff`, runnable examples |
| **7 — Community** | On-ramp, channels, RFCs | issue/PR templates, this roadmap, [RFC template](https://github.com/rosualinpetru/addlib/tree/main/docs/rfcs) |
| **8 — Maintenance** | Bus factor, ADRs, sustainability | ADRs + design doc as release-blocking artifacts, [`MAINTAINERS.md`](https://github.com/rosualinpetru/addlib/blob/main/MAINTAINERS.md), this page |

## The one ordering the roadmap insists on

Testing and security tooling belong at the **front** of the timeline, not the
end. In `addlib` the test suite, fuzzer, sanitizers, and supply-chain workflows
existed before any "feature" beyond `add` — exactly the roadmap's argument that
for a correctness-critical library, testing *is* the security argument.

## Forward roadmap (illustrative)

- **0.2** — a saturating/wrapping `add` variant (seeds the *experimental* tier),
  behind a clearly-marked import.
- **0.3** — vectorized addition over buffers (NumPy protocol); may justify a
  second published Python artifact.
- **0.x → 1.0** — stabilize the API; reach `1.0` aligned with a (hypothetical)
  external review, per [versioning](explanation/versioning.md).
- **C library** — publish `libadd` to conda-forge / vcpkg if and when C
  consumers ask (demand-driven).

Bigger or breaking changes go through the lightweight
[RFC process](https://github.com/rosualinpetru/addlib/tree/main/docs/rfcs).
