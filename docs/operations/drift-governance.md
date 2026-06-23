# Drift Governance

Date: 2026-06-23
Owner: SRE

## Drift Classes

| Class | Examples | Response |
|---|---|---|
| Critical | oMLX production down, secret leak, missing required LaunchAgent program | Immediate restore or rollback |
| Warning | benchmark regression, unexpected manual lane listener, missing skill recommendation | Review and remediate during maintenance |
| Informational | documentation owner/date gap, dormant dependency inventory change | Track in monthly audit |

## Escalation Workflow

1. Run `scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health.json`.
2. Run `scripts/health/drift-detection/check-platform-drift.py --health-json /tmp/local-ai-health.json`.
3. Classify each finding.
4. Restore production first: oMLX on `18080`, Gemma role model registry, Boneman pointers.
5. Document remediation and validation evidence.

## Ownership

| Drift area | Owner |
|---|---|
| AI endpoint/model lane | AI Platform |
| LaunchAgent | macOS Platform |
| GitHub Actions | DevOps |
| Skills and VS Code | AI Tooling |
| Secrets | Security |
| Documentation | Platform Operations |

## Remediation Rules

- Prefer archive over deletion for legacy LaunchAgents.
- Do not promote lab lanes to startup automatically.
- Treat Docker `host.docker.internal` and host `127.0.0.1` as separate boundaries.
- Re-run health and drift checks after remediation.
