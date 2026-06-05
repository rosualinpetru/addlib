# SPDX-License-Identifier: Apache-2.0
"""Unit tests for the high-level Python API."""

from __future__ import annotations

import addlib
from addlib import add, add_floats, c_version


def test_simple_sums() -> None:
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-5, 5) == 0
    assert add(-7, -8) == -15


def test_large_but_in_range() -> None:
    assert add(2**62, 2**62 - 1) == 2**63 - 1
    assert add(-(2**63), 2**63 - 1) == -1


def test_bool_is_accepted_as_int() -> None:
    # bool is a subclass of int; True behaves as 1.
    assert add(True, 1) == 2
    assert add(False, 41) == 41


def test_add_floats_basic() -> None:
    assert add_floats(0.5, 0.25) == 0.75
    assert add_floats(1, 2) == 3.0  # ints promoted to float


def test_version_consistency() -> None:
    # The native core and the Python package must report the same version.
    assert c_version() == addlib.__version__
