# ADR-0001: Use the Apache License 2.0

- Status: Accepted
- Date: 2026-06-04

## Context

We must pick a license before the first public push (Phase 0.1). The candidate
audience is broad industrial + community adoption. Options considered: MIT,
Apache-2.0, BSD-3, MPL-2.0, LGPL/GPL.

## Decision

License the project under **Apache-2.0**.

## Rationale

- Permissive → zero adoption friction; preferred by corporate legal teams.
- Explicit **patent grant** and retaliation clause — the property MIT/BSD lack,
  and the reason the roadmap recommends Apache-2.0 for an industry-aimed crypto
  library. (For an addition library the patent surface is nil, but we follow the
  recommended default so the example is faithful.)
- It is the default foundations (Apache, Linux Foundation, OpenSSF) expect.

## Alternatives / close call

**Dual MIT OR Apache-2.0** is the de-facto standard in the ZK/crypto ecosystem
and maximizes compatibility. If `addlib` ever needs to vendor into MIT-only
ecosystems, revisit with a follow-up ADR. The cost of dual-licensing is only a
little more LICENSE paperwork.

## Consequences

- `LICENSE` holds the verbatim Apache-2.0 text; `NOTICE` holds the copyright.
- Source files carry `SPDX-License-Identifier: Apache-2.0` headers.
- CI runs a dependency-license check to ensure no incompatible (e.g. GPL)
  dependency sneaks in.
