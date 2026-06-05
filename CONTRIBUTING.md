# Contributing to addlib

Thanks for your interest! This guide gets you from a clean checkout to a merged
pull request.

## TL;DR

```bash
make dev      # create venv, install build + dev dependencies, build the extension
make test     # run the C tests and the Python test suite
make lint     # clang-format + clang-tidy (C), ruff + mypy (Python)
make bench    # run benchmarks
```

## 1. Development environment

You need a C compiler (clang or gcc), CMake ≥ 3.15, and Python ≥ 3.9.

```bash
make dev
source .venv/bin/activate
```

`make dev` is idempotent: it creates `.venv`, installs the project in editable
mode with the `[dev]` extra, and compiles the CFFI extension against the C core
in [`c/`](c/).

To build *only* the standalone C library (the `libadd` artifact, no Python):

```bash
cmake -S . -B build -DADDLIB_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

## 2. Branching and commits

- We use **trunk-based development**: branch off `main`, keep branches short,
  open a PR early. `main` is always releasable and protected.
- We use **[Conventional Commits](https://www.conventionalcommits.org/)**. The
  type drives automated changelog generation and the SemVer bump:

  | Prefix | Meaning | Version bump |
  | --- | --- | --- |
  | `fix:` | bug fix | PATCH |
  | `feat:` | new feature | MINOR |
  | `feat!:` / `BREAKING CHANGE:` | breaking change | MAJOR |
  | `docs:` `test:` `ci:` `build:` `refactor:` `perf:` `chore:` | no release | — |

  Example: `feat(core): add saturating addition variant`

## 3. Developer Certificate of Origin (DCO)

We do **not** require a CLA. Instead, every commit must be signed off under the
[Developer Certificate of Origin](https://developercertificate.org/). This is a
one-line statement that you have the right to submit the contribution:

```bash
git commit -s -m "fix(core): reject NaN inputs in add_floats"
```

`-s` appends a `Signed-off-by: Your Name <you@example.com>` trailer. CI rejects
unsigned commits. Set your identity once with:

```bash
git config user.name  "Your Name"
git config user.email "you@example.com"
```

We also encourage (and for maintainers, require) **signed commits** (`git commit -S`) — see [SECURITY.md](SECURITY.md).

## 4. Tests are required

Changes need tests.

- New behavior → add unit tests and, where applicable, property-based tests.
- Bug fix → add a regression test that fails before your fix.
- The adversarial / negative tests (e.g. overflow must raise) and the
  known-answer tests are **release-blocking gates**; never weaken them to make
  a change pass.

See [docs/explanation/testing.md](docs/explanation/testing.md) for the testing
strategy.

## 5. Pull request checklist

- [ ] Commits are signed off (`-s`) and follow Conventional Commits.
- [ ] `make lint` and `make test` pass locally.
- [ ] New/changed public API has docstrings and reference docs.
- [ ] Behavioral changes are noted (the changelog is generated from commits, so
      a good commit message is enough).
- [ ] No security-sensitive report in a public PR/issue — use
      [SECURITY.md](SECURITY.md) instead.

## 6. Review

A maintainer will respond — even if only "we'll look this week" — quickly. One
approving review from a maintainer other than the author plus green CI is
required to merge. See [GOVERNANCE.md](GOVERNANCE.md).

## Reporting bugs and requesting features

Use the issue templates. For anything security-sensitive, follow
[SECURITY.md](SECURITY.md) — **never** file a vulnerability as a public issue.
