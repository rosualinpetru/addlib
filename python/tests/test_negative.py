# SPDX-License-Identifier: Apache-2.0
"""Adversarial / must-reject tests — the release-blocking gate.

A high-value, often-skipped investment is the suite that *tries to make the
system accept something it must reject*. For addition, "rejection" means:
overflow must raise, out-of-range inputs must raise, and wrong types must raise
— never silently return a wrong or wrapped answer. Weakening any of these is
treated like shipping a crash.
"""

from __future__ import annotations

import pytest

from addlib import AdditionOverflowError, add, add_floats

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1


@pytest.mark.negative
@pytest.mark.parametrize(
    ("a", "b"),
    [
        (INT64_MAX, 1),
        (INT64_MAX, INT64_MAX),
        (INT64_MIN, -1),
        (INT64_MIN, INT64_MIN),
        (2**62, 2**62),  # 2**63, just over the edge
    ],
)
def test_overflow_must_raise(a: int, b: int) -> None:
    with pytest.raises(AdditionOverflowError):
        add(a, b)


@pytest.mark.negative
@pytest.mark.parametrize("bad", [2**63, -(2**63) - 1, 2**100, -(2**128)])
def test_out_of_range_inputs_must_raise(bad: int) -> None:
    with pytest.raises(AdditionOverflowError):
        add(bad, 0)
    with pytest.raises(AdditionOverflowError):
        add(0, bad)


@pytest.mark.negative
@pytest.mark.parametrize("bad", ["1", 1.0, None, 1 + 2j, b"1", [1], 3.5])
def test_int_type_errors(bad: object) -> None:
    with pytest.raises(TypeError):
        add(bad, 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        add(1, bad)  # type: ignore[arg-type]


@pytest.mark.negative
@pytest.mark.parametrize("bad", ["x", None, [1.0], object(), b"x", 1 + 0j])
def test_float_type_errors(bad: object) -> None:
    with pytest.raises(TypeError):
        add_floats(bad, 1.0)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        add_floats(1.0, bad)  # type: ignore[arg-type]


@pytest.mark.negative
def test_overflow_error_is_overflow_error_subclass() -> None:
    # Callers catching the built-in OverflowError must keep working.
    assert issubclass(AdditionOverflowError, OverflowError)
    with pytest.raises(OverflowError):
        add(INT64_MAX, 1)
