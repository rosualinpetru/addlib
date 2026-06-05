# Testing strategy

For a library that ships a compiled extension, tests are part of the *correctness
and safety argument*, not just QA. `addlib` models that discipline at small scale.

## The pyramid

| Layer | Where | What it does |
| --- | --- | --- |
| **Unit** | `python/tests/test_addition.py`, `c/tests/test_add.c` | Every function, happy path + edges. |
| **Known-answer** | `python/tests/test_kat.py` | Fixed input→output vectors — an exact-value regression guard. |
| **Property-based** | `python/tests/test_properties.py` | Invariants over a huge space (Hypothesis), cross-validated against Python's exact integer arithmetic. |
| **Negative / adversarial** | `python/tests/test_negative.py` | *Must-reject* cases: overflow, out-of-range, wrong types. **Release-blocking.** |
| **ABI contract** | `python/tests/test_abi_contract.py` | Exercises the C ABI directly, incl. the NULL-output path. |

## Release-blocking gates

The `negative` and `kat` markers flag tests that must never be weakened to make
a change pass — treat a regression there like a crash. Run just those:

```bash
pytest -m negative
pytest -m kat
```

## C correctness under sanitizers

The C tests run under AddressSanitizer + UndefinedBehaviorSanitizer in CI and
under Valgrind nightly. The implementation is written to be *total* — no input
triggers undefined behavior — which is the property the fuzzer verifies.

## Fuzzing

`c/fuzz/fuzz_add.c` is a libFuzzer target over the "bytes → result" path
(attacker-controlled input is where memory-safety bugs surface). It uses a
**128-bit differential oracle**: `__int128` addition can't overflow two `int64`
values, so it pins the exact expected status and result for every input. Runs
nightly.

Run it locally with `make fuzz`. On **macOS**, Apple's bundled clang does not
ship the libFuzzer runtime, so use Homebrew LLVM:

```bash
brew install llvm
make fuzz FUZZ_CC="$(brew --prefix llvm)/bin/clang"
```

## Correctness under approximation

`add_floats` is approximate (IEEE-754 rounding). All float comparisons go
through `addlib.testing.approx_equal` with one documented tolerance, so
"correct" has a single, precise meaning across the suite.

## Benchmarks

`benchmarks/bench_addition.py` tracks per-call cost with `pytest-benchmark`;
the nightly job stores the JSON so trends are visible over time.
