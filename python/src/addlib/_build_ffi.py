# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""CFFI build script: compiles the ``libadd`` C core into the ``addlib._add_cffi``
extension module (CFFI "API, out-of-line" mode).

This is the bridge between the stable C ABI in ``c/include/add/add.h`` and the
high-level Python API in :mod:`addlib.core`. The ``cdef`` block below MUST stay
in sync with that header — it is the Python-visible projection of the C-ABI
contract. A test (``test_abi_contract``) checks that the symbols line up.

We compile the C *sources* directly into the extension so the resulting wheel is
self-contained (no need for ``libadd`` to be installed on the user's system).
The standalone ``libadd`` shared library is built separately via CMake for C/C++
consumers; see ``c/CMakeLists.txt``.
"""

from __future__ import annotations

import os

from cffi import FFI

ffibuilder = FFI()

# --- The C-ABI surface, as seen by Python -------------------------------------
# Keep in sync with c/include/add/add.h. CFFI understands the <stdint.h> types
# (int64_t, ...). Enum values are exposed on the compiled module as lib.ADD_OK,
# lib.ADD_ERR_OVERFLOW, etc.
ffibuilder.cdef(
    """
    typedef enum add_status {
        ADD_OK = 0,
        ADD_ERR_NULL = 1,
        ADD_ERR_OVERFLOW = 2
    } add_status_t;

    add_status_t add_i64(int64_t a, int64_t b, int64_t *out);
    double add_f64(double a, double b);
    const char *add_version(void);
    """
)


def _c_dir() -> str:
    """Return the C directory as a path *relative to the build cwd*.

    setuptools requires an extension's ``sources`` to be relative to the
    ``setup.py`` directory and rejects absolute paths. Every PEP 517 frontend
    (pip, build, cibuildwheel) runs the backend with the project root — or, for
    an sdist build, the unpacked sdist root — as the working directory, and both
    layouts contain ``c/`` at the top level. So the plain literal ``"c"`` is the
    correct, portable answer; we only fall back to locating relative to this
    file (and re-relativizing) if that is somehow not the case.
    """
    if os.path.isdir(os.path.join("c", "include", "add")):
        return "c"
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.normpath(os.path.join(here, "..", "..", "..", "c")),
        os.path.join(here, "_c"),  # a future vendored copy beside the package
    ]
    for cand in candidates:
        if os.path.isdir(os.path.join(cand, "include", "add")):
            return os.path.relpath(cand)
    raise RuntimeError(
        "Cannot locate the libadd C sources. Looked in: 'c' and:\n  "
        + "\n  ".join(candidates)
    )


_C = _c_dir()


def _read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# Compile the canonical C implementation *in-line* into the extension rather than
# passing it as a separate `sources` entry. A separate cross-directory source gets
# absolutized somewhere in the cffi/setuptools build and is then rejected by
# setuptools' build_py manifest pass (assert_relative). Inlining the source body
# keeps the wheel self-contained and side-steps that entirely; the header is still
# resolved via include_dirs, and the standalone libadd CMake build compiles the
# very same add.c, so there is no duplicated implementation.
ffibuilder.set_source(
    "addlib._add_cffi",
    _read_text(os.path.join(_C, "src", "add.c")),
    include_dirs=[os.path.join(_C, "include")],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
