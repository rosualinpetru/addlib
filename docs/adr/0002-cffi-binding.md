# ADR-0002: Expose the C core via a CFFI ABI

- Status: Accepted
- Date: 2026-06-04

## Context

The core is pure C. We must choose how Python talks to it. Options:
pybind11, Cython, CFFI, PyO3+Rust, raw CPython API.

## Decision

Use **CFFI** in *API, out-of-line* mode. A documented C ABI
(`c/include/add/add.h`) is the contract; the bindings sit on top of it.

## Rationale

- Best match for a pure-C core (no C++ toolchain dependency pulled in).
- Keeps the C library reusable independently of Python — the contract is the
  header, not the binding.
- "API out-of-line" compiles a real extension module, so we get a fast, normal
  import and self-contained wheels.

## Alternatives

- **pybind11/Cython**: pull in C++ or a second language; unnecessary here.
- **PyO3 + Rust**: attractive for memory safety, but would mean rewriting the
  core in Rust. Out of scope for this example; revisit only if the core moves to
  Rust.

## Consequences

- The `cdef` in `_build_ffi.py` duplicates the header's declarations; a test
  guards that they agree.
- Adding/changing a C function requires updating both `add.h` and the `cdef`.
