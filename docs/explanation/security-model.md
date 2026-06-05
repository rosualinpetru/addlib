# Security model

A short, honest statement of what `addlib` does and does not protect. For an
addition library it is deliberately small, but writing it down is the discipline
worth copying into a real project.

## What the library does

`addlib` computes `a + b` for signed 64-bit integers (checked) and IEEE-754
doubles (approximate). That is the entire functional surface.

## Threat model

| Question | Answer |
| --- | --- |
| Does it process secret/sensitive data? | **No.** Inputs are ordinary numbers. There is nothing to keep confidential, so side-channel/timing concerns do not apply here. |
| What can untrusted input do? | The only untrusted-input path is the C code turning bytes/arguments into a result. The risk class is **memory safety / undefined behavior**. |
| What is the correctness guarantee? | `add_i64` either returns the mathematically exact sum or signals `ADD_ERR_OVERFLOW`; it never returns a wrong or silently-wrapped value. `add_f64` returns the correctly-rounded IEEE-754 sum. |

## In scope

- **Memory safety of the C core.** Mitigated by: a total implementation (no
  input triggers UB), ASan/UBSan in CI, Valgrind nightly, and a libFuzzer target
  with a 128-bit oracle.
- **Correctness.** Mitigated by known-answer tests, property-based tests, and
  release-blocking negative tests (overflow and bad input must be rejected).
- **Supply-chain integrity.** The part that matters even for a trivial
  dependency — see below.

## Out of scope

- Confidentiality / data protection (no secrets are handled).
- Arbitrary-precision arithmetic (use Python `int`; we bound to int64 on purpose
  and reject out-of-range inputs loudly).
- Concurrency hazards: the functions are pure and reentrant; no shared state.

## Supply chain

The realistic attack surface for a small dependency is the *build and
distribution path*, not the code. Controls:

- **Signed releases** via Sigstore + published checksums.
- **PyPI Trusted Publishing** (OIDC) — no long-lived token.
- **SBOM** (CycloneDX) attached to every release.
- **Provenance attestations** (SLSA / GitHub artifact attestations).
- **Branch protection + signed commits + 2FA** for maintainers.
- **Dependency scanning** (Dependabot) and a minimal dependency surface
  (runtime dep: just `cffi`).
- **OpenSSF Scorecard** running on the repo.

See [releasing.md](releasing.md) and the workflows in `.github/workflows/`.

## Audit status

**Unaudited.** This is an example/template project and makes no
production-readiness claim. A real project would state here what has and has not
been independently reviewed — overclaiming is worse than disclosing the gap.
