# SPDX-License-Identifier: Apache-2.0
"""Known-Answer Tests (KATs): fixed inputs with expected outputs.

The crypto-specific layer ordinary software skips. For a real library these
would be published vectors; here they pin exact integer sums and document the
IEEE-754 rounding of specific float sums so a regression is impossible to miss.
"""

from __future__ import annotations

import pytest

from addlib import add, add_floats

INT_VECTORS = [
    (0, 0, 0),
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
    (-10, -20, -30),
    (123_456_789, 987_654_321, 1_111_111_110),
    (2**63 - 2, 1, 2**63 - 1),  # largest representable result
    (-(2**63), 0, -(2**63)),  # smallest representable input
]

FLOAT_VECTORS = [
    (0.0, 0.0, 0.0),
    (0.5, 0.25, 0.75),
    (1.0, 2.0, 3.0),
    (-2.5, 2.5, 0.0),
    (0.1, 0.2, 0.30000000000000004),  # documents binary floating-point rounding
]


@pytest.mark.kat
@pytest.mark.parametrize(("a", "b", "expected"), INT_VECTORS)
def test_integer_known_answers(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected


@pytest.mark.kat
@pytest.mark.parametrize(("a", "b", "expected"), FLOAT_VECTORS)
def test_float_known_answers(a: float, b: float, expected: float) -> None:
    # Exact equality on purpose: these are the precise IEEE-754 results.
    assert add_floats(a, b) == expected
