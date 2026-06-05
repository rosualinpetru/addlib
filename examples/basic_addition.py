# SPDX-License-Identifier: Apache-2.0
"""The smallest end-to-end example: import addlib and add some numbers.

Run it:  python examples/basic_addition.py
This script is executed in CI (see python/tests/test_examples.py) so it can't rot.
"""

from __future__ import annotations

from addlib import AdditionOverflowError, add, add_floats
from addlib.testing import approx_equal


def main() -> None:
    print("add(2, 3)            =", add(2, 3))
    print("add(-10, 4)          =", add(-10, 4))
    print("add_floats(0.5, 0.25)=", add_floats(0.5, 0.25))

    # Float results are approximate — compare with a tolerance.
    assert approx_equal(add_floats(0.1, 0.2), 0.3)

    # Overflow is rejected, never wrapped.
    try:
        add(2**63 - 1, 1)
    except AdditionOverflowError as exc:
        print("overflow correctly rejected:", exc)


if __name__ == "__main__":
    main()
