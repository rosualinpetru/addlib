# Vulnerability disclosure runbook

Write the workflow down *before* you need it — a panic during a live disclosure
is how mistakes happen (Phase 4.3). This is the maintainer-facing companion to
the user-facing [SECURITY.md](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md).

## Roles

- **Triager** — first maintainer to see the report; acknowledges and does the
  initial assessment.
- **Fix owner** — maintainer who develops the patch (often the triager).
- **Release manager** — maintainer who cuts the patched release and publishes
  the advisory.

(On a small team one person may wear all three hats; name them per incident in
the private advisory thread.)

## Timeline

| When | Action |
| --- | --- |
| T + 0 | Report arrives via GitHub Private Vulnerability Reporting or `security@`. |
| ≤ 72 h | Triager **acknowledges** receipt to the reporter. |
| ≤ 7 d | Triage: confirm/repro, assess severity (CVSS), decide in/out of scope. |
| during | Open a **draft GitHub Security Advisory** (private). Work the fix on a private fork/branch linked to the advisory. |
| during | If warranted, **request a CVE** through GitHub (GitHub is a CNA). |
| ≤ 30 d | Fix ready, reviewed, regression test added (this test becomes a permanent gate). |
| embargo end | Default embargo **90 days** or sooner by agreement with the reporter. |
| release | Release manager ships the patched version (see [releasing.md](releasing.md)), then **publishes the advisory** and credits the reporter. |

## Fix & release mechanics

1. Land the fix on the supported line(s). Pre-1.0 that is **latest only**; once
   we maintain older lines, backport to their release branches.
2. The fix ships as a **PATCH** release and is announced via the advisory.
3. Update [`CHANGELOG.md`](https://github.com/rosualinpetru/addlib/blob/main/CHANGELOG.md) under a `### Security` heading,
   referencing the CVE/advisory ID.
4. Bump [`SECURITY.md`](https://github.com/rosualinpetru/addlib/blob/main/SECURITY.md)'s supported-versions table if needed.

## After the fact

- Hold a short blameless retro: how did it get in, did a test gap let it
  through, what guard prevents recurrence?
- Keep the regression test forever.

## Coordinates

- Private reporting: repo **Security → Report a vulnerability**.
- Email fallback: `rosualinpetru@gmail.com` (placeholder — replace before going
  public).
