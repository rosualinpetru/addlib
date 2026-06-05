# Security model

A short, honest statement of what `addlib` does and does not protect — the
Phase 4.1 discipline. For a cryptographic library this section pre-answers the
questions every auditor asks; for an addition library it is deliberately small,
but the *structure* is the point.

## What the library does

`addlib` computes `a + b` for signed 64-bit integers (checked) and IEEE-754
doubles (approximate). That is the entire functional surface.

## Threat model

| Question | Answer |
| --- | --- |
| Does it process secrets? | **No.** Inputs are ordinary numbers, not keys or plaintexts. |
| Is timing/side-channel resistance required? | **No** — there are no secrets, so there is nothing to leak through timing. `add_i64` does branch on values (overflow check); this is fine *here* and would **not** be acceptable for a secret-dependent operation. The point is documented so the assumption is explicit. |
| What can untrusted input do? | The only untrusted-input path is the C function turning bytes/arguments into a result. The risk class is **memory safety / undefined behavior**, not confidentiality. |
| What is the integrity guarantee? | `add_i64` either returns the mathematically exact sum or signals `ADD_ERR_OVERFLOW`; it never returns a wrong or silently-wrapped value. `add_floats` returns the correctly-rounded IEEE-754 sum. |

## What is in scope

- **Memory safety of the C core.** Mitigated by: a total implementation (no
  input triggers UB), ASan/UBSan in CI, Valgrind nightly, and a libFuzzer target
  with a 128-bit oracle.
- **Correctness / "soundness".** Mitigated by KATs, property-based tests, and
  release-blocking negative tests (overflow and bad input must be rejected).
- **Supply-chain integrity.** This is the part that genuinely matters even for a
  trivial library — see [supply chain](#supply-chain), below.

## What is out of scope

- Confidentiality / side-channel resistance (no secrets).
- Arbitrary-precision arithmetic (use Python `int` for that; we bound to int64
  on purpose and reject out-of-range inputs loudly).
- Concurrency hazards: the functions are pure and reentrant; there is no shared
  state.

## Constant-time note

No operation in `addlib` is constant-time, and none needs to be, because none
touches a secret. If a future variant ever operates on secret data, it must be
re-evaluated against a constant-time requirement and this document updated.

## Supply chain

The realistic attack surface for a tiny dependency is the *build and
distribution path*, not the code. Controls (Phase 4.2):

- **Signed releases** via Sigstore/cosign + published checksums.
- **PyPI Trusted Publishing** (OIDC) — no long-lived token.
- **SBOM** (CycloneDX) attached to every release.
- **Provenance attestations** (SLSA / GitHub artifact attestations).
- **Branch protection + signed commits + 2FA** for maintainers.
- **Dependency scanning** (Dependabot) and a minimal dependency surface
  (runtime dep: just `cffi`).
- **OpenSSF Scorecard** running on the repo.

See [releasing.md](releasing.md) and the workflows in `.github/workflows/`.

## Audit status

**Unaudited.** This is an example project. A real library would state here what
has and has not been independently reviewed, and would not claim
production-readiness before a focused external review of the soundness-critical
code. Overclaiming is worse than disclosing the gap.
