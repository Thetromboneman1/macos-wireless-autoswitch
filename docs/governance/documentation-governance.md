# Documentation Governance

Date: 2026-06-23

## Canonical Structure

| Area | Canonical location |
|---|---|
| Current operations | `docs/operations/` |
| Current architecture | `docs/architecture/` |
| macOS automation | `docs/macos/` |
| Security and secrets | `docs/security/` |
| Benchmarks and stability | `docs/benchmarks/` |
| Historical implementation reports | `docs/autonomous-modernization/` |
| External reference snapshots | `docs/reference/` |

## Current Canonical Docs

- `docs/architecture/ai-service-catalog.md`
- `docs/architecture/startup-orchestration-v2.md`
- `docs/operations/platform-maintenance-v2.md`
- `docs/operations/platform-drift-detection.md`
- `docs/operations/swap-pressure-remediation-phase2.md`
- `docs/macos/launchagent-legacy-cleanup.md`
- `docs/security/secret-inventory.md`
- `docs/security/onepassword-secrets.md`

## Historical Docs

`docs/autonomous-modernization/` remains useful for evidence, dated decisions, and benchmark provenance. Do not treat every older report as current policy; current policy lives in the canonical structure above.

## Review Cadence

| Cadence | Review |
|---|---|
| Monthly | Operations, drift, LaunchAgents, secrets pointers |
| Quarterly | Benchmark docs, service catalog, startup orchestration |
| After major changes | Update current docs and add a dated implementation report only when it adds evidence |

## Ownership

The user owns platform direction and approvals. Codex may update docs when it validates live machine state and keeps generated historical reports clearly dated.
