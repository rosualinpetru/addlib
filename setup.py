# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alin-Petru Roșu
"""Minimal setup shim.

All static metadata lives in ``pyproject.toml``. This file exists only to wire
up CFFI's setuptools integration: ``cffi_modules`` tells setuptools to import
``ffibuilder`` from the build script and compile the ``addlib._add_cffi``
extension. The path is relative to the project root (where this file lives),
which holds both for a source checkout and for a build from the sdist.
"""

from setuptools import setup

setup(
    cffi_modules=["python/src/addlib/_build_ffi.py:ffibuilder"],
)
