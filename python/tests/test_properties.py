# SPDX-License-Identifier: Apache-2.0
"""Property-based tests (Hypothesis).

The crypto analogue: instead of (or in addition to) fixed vectors, assert
invariants over a huge input space the fuzzer-style engine explores. Here the
"reference implementation" we cross-validate against is Python's own arbitrary-
precision integer arithmetic.
"""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from addlib import AdditionOverflowError, add, add_floats
from addlib.testing import approx_equal

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1
int64 = st.integers(min_value=INT64_MIN, max_value=INT64_MAX)
# Bounded so that a+b cannot overflow IEEE-754 double to infinity.
finite = st.floats(
    allow_nan=False, allow_infinity=False, min_value=-1e150, max_value=1e150
)


@given(int64, int64)
def test_matches_reference_integer_addition(a: int, b: int) -> None:
    true_sum = a + b  # exact, arbitrary precision
    if INT64_MIN <= true_sum <= INT64_MAX:
        assert add(a, b) == true_sum
    else:
        with pytest.raises(AdditionOverflowError):
            add(a, b)


@given(int64, int64)
def test_integer_commutativity(a: int, b: int) -> None:
    try:
        ab = add(a, b)
    except AdditionOverflowError:
        # Commutativity must hold for the *failure* mode too.
        with pytest.raises(AdditionOverflowError):
            add(b, a)
    else:
        assert ab == add(b, a)


@given(int64)
def test_integer_identity(a: int) -> None:
    assert add(a, 0) == a
    assert add(0, a) == a


@given(finite, finite)
def test_float_commutativity(a: float, b: float) -> None:
    # Float addition is exactly commutative (same rounding both ways).
    assert add_floats(a, b) == add_floats(b, a)


@given(finite)
def test_float_identity_within_tolerance(a: float) -> None:
    assert approx_equal(add_floats(a, 0.0), a)
