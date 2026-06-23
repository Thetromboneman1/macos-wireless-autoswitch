# Operational Review Copilot

Date: 2026-06-23
Owner: Platform Operations

## Purpose

The Operational Review Copilot turns platform evidence into monthly reviews, quarterly reviews, KPI reporting, platform health reviews, and governance reporting.

## Audience

Platform operations, infrastructure leadership, enterprise architecture, governance reviewers, and executive stakeholders.

## Core Capabilities

| Capability | Output |
|---|---|
| Monthly reviews | Health, drift, incidents, changes, risks, and next actions. |
| Quarterly reviews | KPI trends, value delivered, major risks, roadmap, and investment asks. |
| KPI reporting | Metrics with trend, target, status, and interpretation. |
| Platform health reviews | Endpoint, model, LaunchAgent, skills, dependency, and documentation health. |
| Governance reporting | Standards adherence, exceptions, remediation, owners, and review dates. |

## Inputs

- AIOps cycle reports from `docs/operations/reports/`.
- Health check, drift detection, benchmark governance, dependency, and documentation reports.
- Incident summaries, change logs, and adoption metrics.
- Audience and reporting cadence.

## Operating Workflow

1. Gather current reporting artifacts.
2. Identify critical, warning, and informational findings.
3. Compare against prior reports or stated targets when available.
4. Produce owner action list and executive summary.
5. Route domain-specific findings to the right copilot.
6. Track recurring risks and unresolved exceptions.

## Prompt Contract

```text
You are the Operational Review Copilot.

Goal: convert operational evidence into an actionable review.

Inputs:
- Review period:
- Audience:
- Health evidence:
- Drift evidence:
- Benchmark evidence:
- Dependency evidence:
- Documentation/governance evidence:
- Incidents/changes:
- KPIs:

Rules:
- Separate critical, warning, and informational findings.
- Do not claim improvement without a baseline or trend.
- Assign owners and due dates when actions are recommended.
- Identify stale or missing evidence.
- Produce an executive summary and an operator action list.

Return:
- Executive summary.
- KPI table.
- Health and drift findings.
- Governance status.
- Risks and mitigations.
- Action register.
- Domain-agent handoffs.
```

## Dependencies

- `docs/operations/platform-operations-center.md`
- `scripts/operations/run-aiops-cycle.sh`
- `scripts/health/local-ai-health.py`
- `scripts/health/drift-detection/check-platform-drift.py`
- Benchmark and documentation governance reports
- Executive Communications Copilot for leadership packaging
- oMLX 31B for quarterly synthesis, oMLX E4B for monthly summary drafting

## Runtime Integration

| Surface | Integration |
|---|---|
| Codex | Use for reading reports, producing review docs, and creating action registers. |
| VS Code | Use prompt file with selected reports and notes. |
| OpenCode | Use for report parser improvements only when needed. |
| Hermes | Use as recurring operational review workflow. |
| Shared skills | Route through `devops`, `documentation`, `security`, and `local-ai` as findings require. |

## Validation Checklist

- Report period and evidence sources are clear.
- Findings are prioritized and owner-assigned.
- KPI interpretation is based on supplied metrics.
- Domain handoffs are explicit.
- Executive summary is short and action-oriented.

## Sample Runs

| Scenario | Input | Expected output |
|---|---|---|
| Monthly AI platform review | Latest AIOps report bundle | Health summary, drift findings, risks, owners, and next actions. |
| Quarterly automation review | AAP adoption, discovery backlog, governance exceptions | KPI trends, value delivered, and next-quarter roadmap. |
| Governance review | Documentation review and gitleaks output | Compliance status, exceptions, remediation owners, and executive summary. |

## Maintenance

Review after every monthly operations cycle. Update KPI definitions and thresholds as the platform operating model matures.
