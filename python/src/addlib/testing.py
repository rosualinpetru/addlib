# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""Comparison helpers for approximate (floating-point) results.

Funnel all float comparisons through one helper with a single, documented
tolerance, so that "approximately equal" has one precise meaning across the
test suite. For ``add_floats`` the only approximation is IEEE-754 rounding.
"""

from __future__ import annotations

import math

# Default tolerances. Documented here so auditors and downstream users can see
# exactly what "approximately equal" means.
DEFAULT_REL_TOL = 1e-12
DEFAULT_ABS_TOL = 1e-12


def approx_equal(
    a: float,
    b: float,
    *,
    rel_tol: float = DEFAULT_REL_TOL,
    abs_tol: float = DEFAULT_ABS_TOL,
) -> bool:
    """Return True if ``a`` and ``b`` are equal within tolerance.

    NaN is never equal to anything (including itself). Infinities are equal only
    to the same infinity. Otherwise this is :func:`math.isclose` with the
    project's default tolerances.
    """
    if math.isnan(a) or math.isnan(b):
        return False
    if math.isinf(a) or math.isinf(b):
        return a == b
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
