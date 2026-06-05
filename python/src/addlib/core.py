# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""High-level, Pythonic API for :mod:`addlib`.

The arithmetic is performed in C (see ``c/src/add.c``); this module is a thin,
misuse-resistant wrapper over the CFFI bindings. Design goal: the safe thing is
the easy thing, and errors are explicit rather than silent.
"""

from __future__ import annotations

from importlib import metadata

from ._add_cffi import ffi, lib

__all__ = [
    "AdditionOverflowError",
    "__version__",
    "add",
    "add_floats",
    "c_version",
]

try:
    __version__ = metadata.version("addlib")
except metadata.PackageNotFoundError:  # imported from a source tree, not installed
    __version__ = "0.0.0+unknown"

# Signed 64-bit bounds. We validate at the Python boundary so callers get a
# clear AdditionOverflowError instead of a generic CFFI marshalling error.
_INT64_MIN = -(2**63)
_INT64_MAX = 2**63 - 1


class AdditionOverflowError(OverflowError):
    """Raised when an integer addition cannot be represented in signed 64 bits.

    Subclasses the built-in :class:`OverflowError`, so existing
    ``except OverflowError`` handlers keep working.
    """


def _as_int(name: str, value: object) -> int:
    if not isinstance(value, int):  # note: bool is a subclass of int and is allowed
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return int(value)


def _as_float(name: str, value: object) -> float:
    # Accept ints and floats (and bool, as an int); reject str and everything
    # else rather than silently coercing — that is the misuse-resistant choice.
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} must be a real number (int or float), got {type(value).__name__}"
        )
    return float(value)


def add(a: int, b: int) -> int:
    """Return ``a + b`` for two signed 64-bit integers, computed in C.

    Args:
        a: First addend. Must fit in signed 64 bits.
        b: Second addend. Must fit in signed 64 bits.

    Returns:
        The exact sum ``a + b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not an :class:`int`.
        AdditionOverflowError: If an input is outside the signed 64-bit range,
            or if the true sum overflows it.

    Example:
        >>> from addlib import add
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
    """
    a = _as_int("a", a)
    b = _as_int("b", b)
    for name, value in (("a", a), ("b", b)):
        if not (_INT64_MIN <= value <= _INT64_MAX):
            raise AdditionOverflowError(
                f"{name}={value} is outside the signed 64-bit range "
                f"[{_INT64_MIN}, {_INT64_MAX}]"
            )

    out = ffi.new("int64_t *")
    status = lib.add_i64(a, b, out)
    if status == lib.ADD_ERR_OVERFLOW:
        raise AdditionOverflowError(f"{a} + {b} overflows the signed 64-bit range")
    if status != lib.ADD_OK:
        # ADD_ERR_NULL is unreachable here (we always pass a valid pointer);
        # surface anything unexpected loudly rather than returning garbage.
        raise RuntimeError(f"add_i64 returned unexpected status {status}")
    return int(out[0])


def add_floats(a: float, b: float) -> float:
    """Return ``a + b`` for two real numbers, computed in C as IEEE-754 doubles.

    Follows IEEE-754 semantics: ``add_floats(float("inf"), 1.0)`` is ``inf`` and
    NaN propagates; no exception is raised for those. Because the result is
    approximate, callers should compare with a tolerance, not for exact
    equality (see :func:`addlib.testing.approx_equal`).

    Args:
        a: First addend (int or float).
        b: Second addend (int or float).

    Returns:
        The IEEE-754 double-precision sum.

    Raises:
        TypeError: If an argument is not a real number.

    Example:
        >>> from addlib import add_floats
        >>> add_floats(0.1, 0.2)
        0.30000000000000004
    """
    af = _as_float("a", a)
    bf = _as_float("b", b)
    return float(lib.add_f64(af, bf))


def c_version() -> str:
    """Return the version string reported by the underlying C core.

    Useful for asserting that the loaded native extension matches the Python
    package version.
    """
    raw: bytes = bytes(ffi.string(lib.add_version()))
    return raw.decode("ascii")
