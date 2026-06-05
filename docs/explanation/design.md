# Technical Design Document

> A living design document, reviewed like code. It is the home for the C-ABI
> contract, the module dependency graph, the artifact decision, the stability
> tiering, and the public-API surface.

## 1. Scope

`addlib` adds two numbers. It exists as a **template and worked example** of a
Python library with a C performance core exposed through a CFFI ABI, carried
through the full lifecycle of an open-source native library: licensing, CI,
testing, security, releasing, docs, community, and maintenance.

The functionality is trivial on purpose. Replace `add_i64`/`add_f64` with your
real performance-critical C and the surrounding structure carries over unchanged.

## 2. The C/Python boundary

- **C** does the work (`c/src/add.c`). It is the performance core and the
  independently reusable artifact.
- **Python** provides the ergonomic, misuse-resistant API
  (`python/src/addlib/core.py`).
- They talk over a **CFFI** ABI (`python/src/addlib/_build_ffi.py`), chosen
  because the core is pure C (no C++).

```
            ┌─────────────────────────────┐
 users  ──▶ │ addlib (Python)             │   high-level, validated, typed
            │   core.py  testing.py       │
            └───────────────┬─────────────┘
                            │  CFFI (API, out-of-line)
            ┌───────────────▼─────────────┐
            │ addlib._add_cffi (compiled) │   generated glue
            └───────────────┬─────────────┘
                            │  C ABI  (add.h)  ◀── the contract
            ┌───────────────▼─────────────┐
            │ libadd (C)                  │   also usable standalone via CMake
            │   add.c  add.h              │
            └─────────────────────────────┘
```

## 3. The C-ABI contract

`c/include/add/add.h` is the **only** surface the bindings depend on, and the
only thing C consumers link against. It is a first-class deliverable.

| Symbol | Signature | Contract |
| --- | --- | --- |
| `add_i64` | `add_status_t add_i64(int64_t, int64_t, int64_t*)` | Checked add; `ADD_ERR_OVERFLOW` if the true sum leaves `int64`; `ADD_ERR_NULL` if out is NULL; never UB. |
| `add_f64` | `double add_f64(double, double)` | IEEE-754 sum; NaN/Inf propagate. |
| `add_version` | `const char *add_version(void)` | Static version string. |
| `add_status_t` | enum `{ADD_OK=0, ADD_ERR_NULL=1, ADD_ERR_OVERFLOW=2}` | Values are ABI; never renumber, only append. |

The CFFI `cdef` block is the Python-visible *projection* of this header. The two
must agree; `tests/test_abi_contract.py` checks the projection compiles and the
symbols/return types behave as declared.

**ABI vs API.** For C consumers the ABI (struct layout, enum values, signatures)
is a separate contract from the source API, versioned by `SOVERSION`
(= MAJOR). Breaking it is a MAJOR event even if Python is unaffected. See
[versioning.md](versioning.md).

## 4. Module / artifact map

Two artifacts from one monorepo:

| Artifact | What | Consumers | Build |
| --- | --- | --- | --- |
| `libadd` | C library + headers + CMake/pkg-config | C/C++ projects | CMake |
| `addlib` | Python package bundling the C core | Python users (`pip install addlib`) | setuptools + CFFI → cibuildwheel |

We **publish the Python wheel** (which bundles the C core, so a user needs no
toolchain) and ship the C library's CMake/pkg-config files for the minority who
want to link `libadd` directly. The internal `c/` vs `python/` split is kept
clean enough to spin the C library out to its own release later without moving
code.

## 5. Stability tiering

Group the public surface by how fast it changes, so the architecture predicts
where breaking changes originate:

| Tier | Members | Stability promise |
| --- | --- | --- |
| **stable** | `add_i64`, `add_f64`, `add_version` and their Python wrappers | SemVer-guaranteed from 1.0; ABI guaranteed by `SOVERSION`. |
| **experimental** | _(none yet)_ — e.g. a future `add_saturating`, vector add | May change in MINOR while pre-1.0; lives behind a clearly-marked import. |

A stable core earns a stability promise first; fast-moving additions stay `0.x`
longer without holding the core back.

## 6. Public API surface (v0)

Python (`addlib`): `add`, `add_floats`, `c_version`, `AdditionOverflowError`,
`__version__`. Plus `addlib.testing.approx_equal` for tolerance-based float
comparison.

C (`libadd`): the three functions and one enum in `add.h`.

Anything not listed is private and may change without notice (CFFI internals,
`_build_ffi`, `_add_cffi`).

## 7. Build-backend decision (a deliberate deviation, documented)

A common recommendation is **scikit-build-core (CMake) + cibuildwheel**. We
deviate for the Python wheel and use **setuptools + CFFI's own build
integration**, because:

1. The binding *is* CFFI, and CFFI generates and compiles its own extension
   module. Driving that through scikit-build-core/CMake adds a layer without
   benefit for a single-source-file core.
2. We still honor "CMake is the lingua franca": `libadd` has a full CMake build
   with install/export/pkg-config for C consumers.
3. cibuildwheel is backend-agnostic, so we keep the recommended wheel matrix.

This is recorded as [ADR-0004](../adr/0004-build-backend.md). If the C core
grows multiple translation units or optional native dependencies, revisit
scikit-build-core.

## 8. Open questions / future

- A saturating or wrapping `add` variant (would seed the `experimental` tier).
- Vectorized `add` over arrays (NumPy buffer protocol) — would change the
  binding ergonomics and might argue for a second published Python artifact.
- Whether to expose `libadd` on conda-forge / vcpkg (demand-driven).
