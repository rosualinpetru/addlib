# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""addlib — integer & float addition with a C core, exposed to Python via CFFI.

A worked example of the VERIFHE open-source library roadmap applied to the
simplest possible shape: a C performance core (``libadd``) called from Python
through a CFFI ABI.

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
