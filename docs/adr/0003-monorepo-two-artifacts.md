# ADR-0003: Monorepo publishing a C library + a Python package

- Status: Accepted
- Date: 2026-06-04

## Context

The central structural decision: one artifact or many? Options:
(A) single Python package, (B) many independent packages, (C) one monorepo
publishing several artifacts.

## Decision

**Option C.** One Git repository. It produces two artifacts:

- `libadd` — the standalone C library (CMake + pkg-config).
- `addlib` — the Python package, which *bundles* the compiled C core.

We publish the Python wheel first; the C library's config files ship for direct
C consumers. The internal `c/` vs `python/` split is kept clean enough to spin
the C library out to its own release cadence later without moving code.

## Rationale

- Atomic cross-cutting refactors (change the ABI and both consumers in one
  commit) while the design is still moving.
- One place for issues, CI, and docs; contributors clone once.
- Preserves the multi-artifact future without paying coordination cost now —
  a pragmatic starting point.

## Consequences

- The sdist must include `c/` so the wheel can compile the core from source.
- Versioning starts **lockstep** (one number) and may move to the hybrid scheme
  (independent C-library version) if cadences diverge — see
  [versioning.md](../explanation/versioning.md).
- A future `vfhe-ring`-style split is a packaging change, not code surgery.
