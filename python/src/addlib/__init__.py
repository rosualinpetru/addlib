# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""addlib — integer & float addition with a C core, exposed to Python via CFFI.

A small example of a Python library backed by a C performance core
(``libadd``) through a CFFI ABI — and a template for packaging and releasing
native (C + Python) libraries.

Public API:
    add(a, b)         -> int     # checked signed-64-bit integer addition (C)
    add_floats(a, b)  -> float   # IEEE-754 double addition (C)
    c_version()       -> str     # version reported by the native core
    AdditionOverflowError         # raised on int64 overflow
"""

from .core import (
    AdditionOverflowError,
    __version__,
    add,
    add_floats,
    c_version,
)

__all__ = [
    "AdditionOverflowError",
    "__version__",
    "add",
    "add_floats",
    "c_version",
]
