# Architecture Decision Records

ADRs capture *why* a decision was made, so the rationale outlives the people who
made it. Per the roadmap's Phase 8.2, these (plus the
[design doc](../explanation/design.md)) are treated as release-blocking
artifacts, not optional docs — they are the project's bus-factor insurance.

Format: one short file per decision, numbered, immutable once `Accepted`
(supersede with a new ADR rather than editing).

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-license-apache-2.0.md) | Use Apache-2.0 | Accepted |
| [0002](0002-cffi-binding.md) | Expose the C core via a CFFI ABI | Accepted |
| [0003](0003-monorepo-two-artifacts.md) | Monorepo publishing a C library + a Python package | Accepted |
| [0004](0004-build-backend.md) | setuptools+CFFI for the wheel; CMake for the C library | Accepted |
