# RFCs (Requests for Comments)

A lightweight design-proposal process for **protocol-level, public-API, or
breaking changes** (roadmap Phase 7.3). Small fixes and additions don't need an
RFC — just open a PR. RFCs exist so big decisions are discussed in the open and
leave a durable rationale trail (which doubles as bus-factor insurance).

## When you need one

- A breaking change to the Python API or the C ABI.
- A new published artifact, or a change to the artifact/versioning strategy.
- Anything you'd want a second maintainer to sign off on the *design* before
  code is written.

## Process

1. Copy [`0000-template.md`](0000-template.md) to
   `NNNN-short-title.md` (use the next free number).
2. Open a PR adding it. Discussion happens on the PR.
3. A maintainer other than the author must approve. Contested RFCs are decided
   per [GOVERNANCE.md](https://github.com/rosualinpetru/addlib/blob/main/GOVERNANCE.md)
   (lead maintainer breaks ties).
4. On acceptance, set `Status: Accepted` and merge. Significant accepted RFCs may
   also be distilled into an [ADR](../adr/README.md).

## Index

| RFC | Title | Status |
| --- | --- | --- |
| — | _none yet_ | — |
