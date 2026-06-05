# Maintenance & sustainability

The phase with no deadline and no glory — and the one that decides whether a
library outlives the burst of effort that created it. `addlib` is an example, so
this page is partly a checklist for *whoever maintains a library shaped like
this*.

## The ongoing load

- **Issue triage.** Label (`bug`, `enhancement`, `triage`, `good-first-issue`),
  prioritize, and apply a stale policy. Triage debt compounds quietly. Aim for a
  fast first response, even just "thanks, we'll look this week."
- **Dependency maintenance.** Dependabot opens grouped update PRs weekly; CI must
  pass before merge. The runtime dependency surface is intentionally tiny
  (`cffi`) — every dependency is attack surface.
- **Toolchain drift.** New Python versions, compilers, and CI OS images break
  native builds over time. The wheel matrix (`cibuildwheel`) and the test matrix
  need periodic bumps just to keep working. Add new CPython versions to
  `pyproject.toml`'s `[tool.cibuildwheel] build` and the CI matrix.
- **Performance vigilance.** The nightly benchmark JSON is there to be *watched*,
  not just collected — a regression in the CFFI-boundary cost should be noticed.
- **Security response.** Keep the [disclosure runbook](disclosure-runbook.md)
  warm and the `security@` intake monitored.

## Bus factor & continuity

The acute risk for any small project: knowledge living in one or two heads.
Mitigations, all already in place here:

- **Write the rationale down.** The [design doc](design.md) and
  [ADRs](../adr/README.md) are treated as **release-blocking** artifacts, not
  optional extras — the highest-leverage continuity investment.
- **Grow maintainers.** The contributor on-ramp (`CONTRIBUTING.md`,
  good-first-issues, responsive review) *is* the succession plan. Trusted
  contributors earn merge rights per
  [GOVERNANCE.md](https://github.com/rosualinpetru/addlib/blob/main/GOVERNANCE.md).
- **Spread the keys.** The maintainer committee holds merge/release rights so no
  single departure halts the project; keep
  [`MAINTAINERS.md`](https://github.com/rosualinpetru/addlib/blob/main/MAINTAINERS.md)
  current.

## Funding & institutional sustainability

For a real library (not this example), the menu is: follow-on grants;
institutional hosting; industry collaboration that converts into co-maintenance
or sponsored features; and supplementary sponsorship
([`FUNDING.yml`](https://github.com/rosualinpetru/addlib/blob/main/.github/FUNDING.yml)).
Sponsorship alone rarely sustains a specialist library — treat it as a
supplement, not the plan.

**Foundation home (close call).** Joining a neutral umbrella adds credibility and
shared infrastructure but also process; it is usually premature early. Revisit
only if/when independent co-maintainers materialize and want neutral governance.

## A note on ordering

Most of what makes maintenance survivable was front-loaded: tests, fuzzing,
sanitizers, supply-chain workflows, and written-down decisions all existed before
the project had more than one function. That is deliberate — see the
[project tour](../ROADMAP.md).
