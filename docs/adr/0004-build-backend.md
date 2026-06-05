# ADR-0004: setuptools+CFFI for the wheel; CMake for the C library

- Status: Accepted
- Date: 2026-06-04

## Context

Phase 2.2 recommends **scikit-build-core (CMake) + cibuildwheel** as the build
backend. Our binding is CFFI (ADR-0002), which generates and compiles its own
extension module. We need a backend that drives CFFI cleanly and still serves
C consumers.

## Decision

- **Python wheel**: PEP 517 build via **setuptools** with CFFI's
  `cffi_modules` integration (a one-line `setup.py` plus metadata in
  `pyproject.toml`). Wheels are built across platforms with **cibuildwheel**.
- **Standalone C library**: a full **CMake** build (`CMakeLists.txt`, install,
  export, pkg-config) — unchanged from the roadmap's intent.

## Rationale

- CFFI owns extension generation; routing it through scikit-build-core/CMake
  adds indirection without benefit for a single-source-file core.
- cibuildwheel is backend-agnostic, so we keep the recommended wheel matrix
  (manylinux, macOS incl. Apple Silicon, Windows) and the sdist fallback.
- "CMake is the lingua franca" is still honored — for the C artifact, which is
  exactly who benefits from it.

## Consequences

- Two build descriptions coexist: `pyproject.toml`+`setup.py` (Python) and
  `CMakeLists.txt` (C). They share the same source in `c/`.
- **Revisit** this ADR if the C core grows multiple translation units, optional
  native dependencies, or platform-specific compilation that CMake expresses
  better than CFFI's `set_source` — at that point scikit-build-core wrapping a
  CMake-built `libadd` becomes the better call.
