# Security Policy

`addlib` is a small library, but it ships a compiled C extension and is a worked
example of a *security-critical* library workflow. We therefore maintain a real
vulnerability-disclosure posture from day one. (See the project's
[security model](docs/explanation/security-model.md) for what is and is not in
scope — for a pure addition library the attack surface is small, but the process
is intentionally identical to what a larger, security-sensitive library would use.)

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report privately through either channel:

1. **GitHub Private Vulnerability Reporting** (preferred) — use the
   *"Report a vulnerability"* button under the repository's **Security** tab.
2. **Email** — `rosualinpetru@gmail.com`.

Please include: affected version(s), platform/architecture, a minimal
reproduction, and the impact you observed (crash, incorrect result, memory
unsafety, etc.).

## Our commitment (SLA)

| Stage | Target |
| --- | --- |
| Acknowledge receipt | within **72 hours** |
| Initial assessment / triage | within **7 days** |
| Fix or mitigation plan | within **30 days** (severity-dependent) |
| Coordinated public disclosure | by mutual agreement; default embargo **90 days** |

We follow coordinated disclosure. We will credit reporters who wish to be
credited in the release notes and the GitHub Security Advisory.

## Supported versions

While the project is pre-1.0, **only the latest released `0.x` line receives
security fixes.** This will be revisited at 1.0, when a support window and
backport policy are defined (see [docs/explanation/versioning.md](docs/explanation/versioning.md)).

| Version | Supported |
| --- | --- |
| `0.1.x` (latest) | ✅ |
| `< 0.1` | ❌ |

## Disclosure workflow

The full triage-to-release runbook lives in
[docs/explanation/disclosure-runbook.md](docs/explanation/disclosure-runbook.md).
