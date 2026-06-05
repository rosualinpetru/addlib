# Versioning policy

## Scheme: Semantic Versioning

`addlib` uses [SemVer](https://semver.org/) — `MAJOR.MINOR.PATCH`:

- **MAJOR** — backward-incompatible API (or C ABI) change.
- **MINOR** — backward-compatible additions.
- **PATCH** — backward-compatible fixes.

### The 0.x signal

We are pre-1.0. While `0.x`, a MINOR bump may break the API — this is honest for
a young library. We will stay `0.x` until the API is genuinely stable, and will
not let any deadline force a premature `1.0`. `1.0` arrives when we can commit to
not breaking the public API casually.

### Stability tiering decides what stabilizes first

Per the [design doc](design.md), `add_i64`/`add_f64` (the *stable* tier) can earn
a stability promise before any future *experimental* variant. The tier predicts
where breaking changes originate.

## Three contracts, versioned separately

1. **Python API** — the functions in `addlib`. Governed by SemVer above.
2. **C ABI** — struct layout, enum values, and signatures in `add.h`. Versioned
   by the library `SOVERSION` (currently `0`), which is **distinct** from the
   release version. Breaking the ABI (e.g. renumbering `add_status_t`, changing a
   signature) is a MAJOR event for C consumers even if the Python API is
   untouched. This is a dimension Python-only projects never face.
3. **Wire / serialization format** — *not applicable* to `addlib` (it serializes
   nothing). Recorded here because the principle matters once a library serializes data:
   anything written by one version must be readable by a compatible one, or the
   incompatibility must be loud. Version such a format with its own
   explicit number, independent of the code API.

## Security patches

A fix for a memory-safety or correctness bug ships as a **PATCH**,
is announced via a security advisory, and — once we support older lines — may be
backported. See the [disclosure runbook](disclosure-runbook.md).

## Single- vs multi-artifact versioning

Today we ship effectively one product (the `addlib` wheel bundles the C core),
so we version **lockstep**: one number, one tag, one changelog. Simple to reason
about.

If/when `libadd` gains an independent release cadence (ADR-0003), we move to a
**hybrid** scheme:

- version the stable C library independently (it changes slowly, earns long-lived
  guarantees);
- let research-active / experimental packages move together;
- publish a one-line compatibility statement per release (e.g.
  `addlib 0.5 requires libadd >= 0.3, < 0.4`) and check the matrix in CI.

Start simple; split when the cadence pain is real, not anticipated.

## Deprecation policy

Never break silently. To remove something: announce it, provide a migration
path, keep the old path working with a `DeprecationWarning` for at least one
MINOR cycle, then remove on a MAJOR. Every breaking change ships with an upgrade
note in the [changelog](https://github.com/rosualinpetru/addlib/blob/main/CHANGELOG.md).

## Supported versions

Pre-1.0: **latest `0.x` only** receives security fixes (see
[SECURITY.md](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md)). A support window and backport policy will be
defined at 1.0 — we will not over-promise support we cannot staff.
