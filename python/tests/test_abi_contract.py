# SPDX-License-Identifier: Apache-2.0
"""Tests that exercise the C ABI directly, below the Python wrapper.

These guard the C-ABI contract documented in docs/explanation/design.md: the
status enum values, the NULL-output error path (which the Python wrapper never
triggers, so it would otherwise be untested), and direct marshalling.
"""

from __future__ import annotations

from addlib._add_cffi import ffi, lib


def test_status_enum_values() -> None:
    # Values are ABI; if these change, it is a breaking change.
    assert int(lib.ADD_OK) == 0
    assert int(lib.ADD_ERR_NULL) == 1
    assert int(lib.ADD_ERR_OVERFLOW) == 2


def test_null_output_pointer_path() -> None:
    # The ADD_ERR_NULL branch, reachable only at the ABI level.
    assert lib.add_i64(1, 2, ffi.NULL) == lib.ADD_ERR_NULL


def test_direct_abi_add() -> None:
    out = ffi.new("int64_t *")
    assert lib.add_i64(40, 2, out) == lib.ADD_OK
    assert out[0] == 42


def test_direct_abi_overflow_leaves_out_untouched() -> None:
    out = ffi.new("int64_t *")
    out[0] = 123
    assert lib.add_i64(2**63 - 1, 1, out) == lib.ADD_ERR_OVERFLOW
    assert out[0] == 123  # contract: unmodified on overflow


def test_version_symbol() -> None:
    # The C core reports a MAJOR.MINOR.PATCH string; don't hardcode the value
    # (test_version_consistency checks it matches the package version).
    v = ffi.string(lib.add_version()).decode("ascii")
    parts = v.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts), v
