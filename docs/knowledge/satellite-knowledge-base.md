# Satellite Knowledge Base

Date: 2026-06-23
Owner: Satellite Platform Owner

## Purpose

This knowledge base supports Satellite Platform Copilot runs for lifecycle management, content views, compliance, upgrades, and governance.

## Source Set

| Source | Use |
|---|---|
| `docs/agents/satellite-platform-agent.md` | Prompt contract, workflow, dependencies, and validation. |
| Lifecycle standards | Host lifecycle phases, patch windows, retirement rules. |
| Content view standards | Promotion, environment, activation key, and repository policy. |
| Compliance requirements | Required baselines, exceptions, reporting cadence. |
| Upgrade guides | Satellite and capsule upgrade sequencing and rollback planning. |
| Governance docs | Risk, SLO, audit, and documentation review requirements. |
| Operations runbooks | Health, drift, capacity, recovery, and reporting context. |

## Capabilities

| Capability | Required evidence | Output |
|---|---|---|
| Lifecycle management | Host groups, lifecycle environments, support dates | Lifecycle review and owner actions |
| Content views | Current content view, promotion state, repo list | Promotion plan and risk notes |
| Compliance | Baseline, scan results, exception list | Compliance summary and remediation path |
| Upgrades | Current version, target version, dependencies, window | Upgrade plan, validation, rollback |
| Governance | Policy, audit, SLO, ownership evidence | Governance-ready review package |

## Retrieval Strategy

1. Start with the Satellite agent prompt.
2. Retrieve lifecycle and content-view standards.
3. Retrieve current operating evidence.
4. Retrieve governance and DR docs for constraints.
5. Produce actions with owner, timing, risk, and validation.

## Maintenance

Refresh during the monthly patch cycle, before upgrades, after lifecycle policy changes, and after compliance reporting changes.
