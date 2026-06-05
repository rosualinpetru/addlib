# SPDX-License-Identifier: Apache-2.0
"""Run the docstring examples in the public API so they can't rot.

Broken examples in a security-adjacent library erode trust fast (roadmap 6.2).
"""

from __future__ import annotations

import doctest

from addlib import core


def test_core_docstring_examples() -> None:
    results = doctest.testmod(core, verbose=False)
    assert results.failed == 0, f"{results.failed} doctest(s) failed"
