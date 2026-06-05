# ADR-0001: Use the Apache License 2.0

- Status: Accepted
- Date: 2026-06-04

## Context

We must pick a license before the first public push. The candidate
audience is broad industrial + community adoption. Options considered: MIT,
Apache-2.0, BSD-3, MPL-2.0, LGPL/GPL.

## Decision

License the project under **Apache-2.0**.

## Rationale

- Permissive → zero adoption friction; preferred by corporate legal teams.
- Explicit **patent grant** and retaliation clause — the property MIT/BSD lack,
  a strong reason to prefer Apache-2.0 for a library aimed at broad industry
  adoption. (For an addition library the patent surface is nil; we use it as a
  sensible default for the template.)
- It is the default foundations (Apache, Linux Foundation, OpenSSF) expect.

## Alternatives / close call

**Dual MIT OR Apache-2.0** is common in parts of the ecosystem and maximizes
compatibility. If `addlib` ever needs to vendor into MIT-only
ecosystems, revisit with a follow-up ADR. The cost of dual-licensing is only a
little more LICENSE paperwork.

## Consequences

- `LICENSE` holds the verbatim Apache-2.0 text; `NOTICE` holds the copyright.
- Source files carry `SPDX-License-Identifier: Apache-2.0` headers.
- CI runs a dependency-license check to ensure no incompatible (e.g. GPL)
  dependency sneaks in.
