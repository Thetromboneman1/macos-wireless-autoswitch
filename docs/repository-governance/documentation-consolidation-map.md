# Documentation Consolidation Map

Date: 2026-06-23

## Canonical Sources

| Topic | Canonical source | Supporting documents | Historical evidence |
|---|---|---|---|
| Local AI architecture | `docs/architecture/ai-service-catalog.md` and `docs/architecture/model-routing.md` | `README.md`, `docs/operations/platform-runbook.md` | `docs/autonomous-modernization/16-unified-ai-platform-architecture.md` |
| oMLX power policy | `docs/OMLX_POWER_POLICY.md` | `scripts/omlx-power-policy.sh`, `scripts/omlx-power-watch.sh` | `docs/autonomous-modernization/26-post-skills-cleanup-and-drift-reconciliation.md` |
| Hermes token/cost controls | `docs/hermes/toolset-optimization.md`, `docs/hermes/prompt-size-toolset-discrepancy.md` | `scripts/operations/hermes-cost-report.py` | `docs/autonomous-modernization/28-hermes-cost-token-context-optimization.md` |
| GitHub Actions governance | `docs/github-actions/actions-estate-inventory.md` | `docs/security/github-actions-security-audit.md`, `docs/operations/github-actions-operations-runbook.md` | `docs/github-actions/workflow-audit.md` |
| Secrets | `docs/security/onepassword-secrets.md` | `docs/security/secret-inventory.md`, `docs/security/github-actions-secrets.md` | dated autonomous-modernization reports |

## Status Rules

- Current docs live in `docs/architecture`, `docs/operations`, `docs/security`, `docs/github-actions`, and `docs/repository-governance`.
- Historical reports stay in `docs/autonomous-modernization` and `docs/local-ai-star-sweep-2026-06-22`.
- Downloaded README snapshots stay in `docs/reference` and are excluded from markdown style lint.
- The only approved 1Password vault name for new references is `Boneman`.
