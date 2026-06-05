# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
At release time the changelog is generated from
[Conventional Commits](https://www.conventionalcommits.org/) and lightly
hand-curated — auto-generated lists alone make poor release notes.

## [Unreleased]

## [0.1.1] — 2026-06-05

### Changed
- Publish **cp314 (Python 3.14) wheels**: upgrade cibuildwheel to v3.4.1 and drop
  the `manylinux2014` image pin so the current default (3.14-capable) image is
  used. `pip install` now needs no compiler on Python 3.14.

## [0.1.0] — 2026-06-04

### Added
- `add(a, b)` — checked signed-64-bit integer addition, computed in C; raises
  `AdditionOverflowError` instead of wrapping.
- `add_floats(a, b)` — IEEE-754 double addition, computed in C.
- `c_version()` and the `AdditionOverflowError` exception.
- `addlib.testing.approx_equal` — tolerance-based float comparison helper.
- Standalone **`libadd`** C library with CMake package config + pkg-config, for
  C/C++ consumers (`SOVERSION` 0).
- CFFI binding (`addlib._add_cffi`) that compiles the C core into a
  self-contained wheel (no toolchain needed to `pip install`).
- Test suite: unit, property-based (Hypothesis), known-answer, adversarial /
  negative (release-blocking), and ABI-contract tests.
- libFuzzer target with a 128-bit differential oracle.
- CI: lint (ruff/mypy/clang-format), cross-platform test matrix, ASan/UBSan C
  build, packaging smoke test; nightly fuzzing, Valgrind, and benchmark trend.
- Supply chain: CodeQL, OpenSSF Scorecard, dependency review, Dependabot.

### Security
- Private vulnerability reporting and a 72-hour acknowledgement SLA
  ([security policy](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md));
  disclosure runbook documented.

[Unreleased]: https://github.com/rosualinpetru/addlib/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/rosualinpetru/addlib/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/rosualinpetru/addlib/releases/tag/v0.1.0
