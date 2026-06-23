# AAP Knowledge Base

Date: 2026-06-23
Owner: AAP Platform Owner

## Purpose

This knowledge base supports the AAP Platform Copilot and Automation Discovery Copilot with automation recommendations, playbook review, upgrade guidance, ROI estimation, and executive reporting.

## Source Set

| Source | Use |
|---|---|
| `docs/agents/aap-platform-agent.md` | AAP prompt contract, workflow, and validation. |
| `docs/agents/automation-discovery-agent.md` | Automation discovery scoring and backlog workflow. |
| AAP standards | Job template, inventory, credential, execution environment, and collection rules. |
| Playbooks and roles | Review quality, idempotency, safety, and reusability. |
| Operational docs | Production support, ownership, incident and rollback patterns. |
| Upgrade guides | Version compatibility, migration paths, testing requirements. |
| Governance docs | Approval, SLO, audit, risk, and security constraints. |

## Capabilities

| Capability | Required evidence | Output |
|---|---|---|
| Automation recommendations | Manual process description, frequency, exception rate, owner | Ranked candidates with implementation path |
| Playbook review | Playbook, inventory model, variables, execution context | Findings, remediation steps, risk notes |
| Upgrade guidance | Current version, target version, dependencies, maintenance window | Upgrade plan, test plan, rollback path |
| ROI estimation | Run frequency, manual duration, labor rate or normalized hour value | Time saved, avoided toil, estimated value |
| Executive reporting | Backlog, delivery status, adoption, risk, ROI evidence | Leadership update with decisions needed |

## Review Rubric

| Dimension | Pass condition |
|---|---|
| Idempotency | Playbook can run repeatedly without unsafe side effects. |
| Safety | Destructive steps are gated, reversible, or explicitly approved. |
| Governance | Credentials, approvals, and audit needs are documented. |
| Reuse | Roles, inventories, and variables avoid one-off hardcoding. |
| Value | Recommendation includes effort, benefit, owner, and next action. |

## Maintenance

Refresh after AAP upgrades, collection changes, major playbook standards changes, or monthly automation backlog review.
