# SPDX-License-Identifier: Apache-2.0
"""Microbenchmarks tracked over time (pytest-benchmark).

Run with: pytest benchmarks --benchmark-only

For the real library these would track prove-time / verify-time / proof-size /
peak memory — the project's headline-risk metrics. Here we track the per-call
overhead of crossing the CFFI boundary, which is the interesting cost for a
trivial core: it tells you how much the binding layer adds over the raw C op.
"""

from __future__ import annotations

from addlib import add, add_floats


def test_bench_add_int(benchmark) -> None:
    result = benchmark(add, 2**40, 2**40)
    assert result == 2**41


def test_bench_add_floats(benchmark) -> None:
    result = benchmark(add_floats, 0.1, 0.2)
    assert abs(result - 0.3) < 1e-9
