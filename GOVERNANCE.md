# Governance

This document records how decisions are made in `addlib`. It is deliberately
lightweight: the project is small, and the goal is to remove ambiguity (and
reduce bus-factor risk) without adding ceremony.

## Model: lead maintainer (sole owner), evolving to a committee

`addlib` currently has a **single owner/maintainer** who holds final say and all
merge/release rights — a lightweight BDFL model, simplest for a one-person
project. As contributors appear, the intent is to grow into a small **maintainer
committee** with a lead maintainer as tie-breaker; the contributor on-ramp is the
succession plan that reduces bus-factor risk.

| Role | Who | Rights |
| --- | --- | --- |
| Lead maintainer / owner | Alin-Petru Roșu ([@rosualinpetru](https://github.com/rosualinpetru)) | Final say; can merge and release |
| Maintainer | _(none yet)_ | Can review, merge, and cut releases |
| Contributor | anyone | Can open issues and PRs |

> Maintainers are listed in [`MAINTAINERS.md`](MAINTAINERS.md).

## Who can do what

- **Merge to `main`** — any maintainer, after the change has at least one
  approving review from a *different* maintainer and CI is green. Branch
  protection enforces this. (While the project has a single maintainer, the owner
  self-merges once CI is green; the second-reviewer rule takes effect as soon as
  there are two maintainers.)
- **Cut a release** — any maintainer may tag a release once the release
  checklist (see [docs/explanation/releasing.md](docs/explanation/releasing.md))
  is satisfied. Releases are produced by CI, not by hand.
- **Add/remove a maintainer** — by consensus of the existing committee; the
  lead maintainer breaks ties.

## Decision-making

1. **Lazy consensus.** Most changes proceed if no maintainer objects within a
   reasonable window (typically 72 hours for non-trivial PRs).
2. **Disputed changes.** If a maintainer objects, the committee discusses on the
   PR or in a GitHub Discussion. If consensus is not reached, the lead
   maintainer decides.
3. **Large or breaking changes** follow the lightweight RFC process
   (see [`docs/rfcs/`](docs/rfcs/)).

## Code of Conduct

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
Enforcement is the responsibility of the maintainer committee.

## Changing this document

Changes to governance are themselves decided by committee consensus and land as
a normal pull request.
