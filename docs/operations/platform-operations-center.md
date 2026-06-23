# Platform Operations Center

Date: 2026-06-23
Owner: Platform Operations

## Purpose

The Platform Operations Center is the single operations view for the local AI platform. It connects service ownership, monitoring, recovery, drift detection, skills, editor integrations, and reporting into one operating model.

## Operations Inventory

| Area | Source of truth | Monitor | Owner | Escalation |
|---|---|---|---|---|
| AI services | `docs/architecture/ai-service-catalog.md` | `scripts/health/local-ai-health.py --skip-chat` | Platform Operations | Restore oMLX first, keep lab lanes manual |
| Model lanes | `config/local-ai-platform/routing-policy.json` | `/v1/models`, benchmark governance | AI Platform | Revert to Gemma role contract |
| LaunchAgents | `docs/macos/launchagent-inventory.md` | health script and drift detector | macOS Platform | Archive stale plists, avoid blind deletion |
| GitHub Actions | `.github/workflows/` | `actionlint`, drift baseline | DevOps | Pin reviewed action versions |
| Health checks | `scripts/health/local-ai-health.py` | AIOps cycle | SRE | Full chat probe only for generation validation |
| Drift detection | `scripts/health/drift-detection/` | AIOps cycle | SRE | Critical, warning, informational workflow |
| Skills | `~/.codex/skills`, `docs/skills/` | health script skill metadata check | AI Tooling | Restart Codex if discovery lags |
| VS Code integrations | `.vscode/` | health script recommendations check | VS Code Platform | Reinstall only missing extensions |
| Secret references | `docs/security/secret-inventory.md` | `gitleaks`, doc review | Security | Use 1Password vault `Boneman` only |

## AIOps Cycle

Run the on-demand operations cycle:

```bash
scripts/operations/run-aiops-cycle.sh
```

Default output:

```text
docs/operations/reports/
```

The cycle runs:

- endpoint-only health;
- drift detection;
- dependency inventory;
- documentation governance review;
- platform report generation;
- optional benchmark comparison when `AIOPS_BENCH_BASELINE` and `AIOPS_BENCH_CURRENT` are set.

## Recovery Procedures

| Symptom | First check | Recovery |
|---|---|---|
| oMLX unavailable | `curl http://127.0.0.1:18080/health` | Restart oMLX, then run authenticated `/v1/models` |
| Missing model role | authenticated `/v1/models` | Restore four-role Gemma contract before changing consumers |
| Port `8002` or `8010` unexpectedly listening | drift report | Confirm lab window or stop manual lane |
| Broken LaunchAgent | health launchagent section | Archive stale plist or restore missing program |
| Skill missing | health `codex_skills` section | Reinstall exact missing skill, restart Codex session |
| VS Code recommendation missing | health `vscode_recommendations` section | Update `.vscode/extensions.json` and validate JSON |
| Secret leak concern | `gitleaks detect --redact` | Remove value, rotate credential, document pointer only |

## Escalation

| Severity | Condition | Response |
|---|---|---|
| Critical | Production oMLX down, secret leak, broken required LaunchAgent | Stop related automation and restore known-good config |
| Warning | Manual lab lane running unexpectedly, benchmark regression, stale dependency | Review within the current maintenance window |
| Informational | Documentation metadata gap, dormant tool inventory change | Queue for monthly maintenance |
