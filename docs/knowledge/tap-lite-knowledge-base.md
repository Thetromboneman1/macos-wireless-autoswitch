# TAP Lite Knowledge Base

Date: 2026-06-23
Owner: Enterprise Architecture

## Purpose

This knowledge base supports Enterprise Architecture Copilot runs for TAP Lite generation, architecture review, risk identification, decision records, and executive summaries.

## Source Set

| Source | Use |
|---|---|
| `TAP-Lite.md` | Current lightweight TAP structure and local example. |
| `docs/agents/enterprise-architecture-agent.md` | Prompt contract and output templates. |
| `docs/architecture/` | Local AI platform, routing, MCP, startup, and knowledge-layer architecture. |
| `docs/governance/` | Governance, audit, risk, SLO, and model promotion requirements. |
| `docs/operations/platform-runbook.md` | Operating constraints and recovery context. |
| `docs/capacity/` | Resource and growth constraints. |
| `docs/disaster-recovery/` | Recovery objectives and restore validation. |

## Capabilities

| Capability | Required evidence | Output |
|---|---|---|
| TAP Lite generation | Business context, current state, target state, constraints, options | TAP Lite package with recommendation and approval path |
| Architecture review | Proposed design, platform standards, governance requirements | Review findings, risks, required changes |
| Risk identification | Architecture, operating model, security and capacity constraints | Risk register with severity, owner, mitigation |
| Decision records | Decision request, options, tradeoffs, consequences | ADR draft with review date |
| Executive summaries | Architecture output plus sponsor audience | One-page leadership summary with decision ask |

## Retrieval Strategy

1. Retrieve the agent prompt and TAP Lite template.
2. Retrieve architecture and governance standards for constraints.
3. Retrieve operations, capacity, and DR docs for implementation realism.
4. Attach current project evidence supplied by the user.
5. Record gaps as open questions instead of inventing facts.

## Quality Bar

- Recommendation is tied to business purpose and platform constraints.
- Risks include owner, mitigation, and review cadence.
- Decision records separate context, options, decision, consequences, and risks.
- Executive summaries contain action needed, timing, benefits, and residual risk.
- All assumptions are labeled.

## Maintenance

Review monthly and after changes to architecture standards, governance rules, model routing, or platform runbooks.
