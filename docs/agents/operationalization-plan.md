# Agent Operationalization Plan

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

This plan converts the documented enterprise agent workforce into repeatable operational agents that produce measurable business value through the existing local AI platform. It is intentionally an execution plan, not a new platform layer, governance framework, or set of agent concepts.

## Runtime Rules

- Production model traffic uses oMLX at `http://127.0.0.1:18080/v1`.
- Reasoning work uses `mlx-community--gemma-4-31b-it-4bit`.
- Coding, document edits, and artifact refinement use `mlx-community--gemma-4-26b-a4b-it-4bit`.
- Fast summaries use `mlx-community--gemma-4-e4b-it-4bit`.
- Routing and classification use `mlx-community--gemma-4-e2b-it-4bit`.
- llama.cpp at `http://127.0.0.1:8002/v1` remains a measured GGUF coding lane only.
- Rapid-MLX at `http://127.0.0.1:8010/v1` remains a manual lab lane only.
- Secrets stay in the Boneman 1Password vault; docs name item references and retrieval methods only.

## Operational Agent Matrix

| Agent | Runtime | Prompt source | Required tools | Required knowledge | Validation strategy |
|---|---|---|---|---|---|
| Enterprise Architecture Copilot | oMLX reasoning, coding for repo edits | `docs/agents/enterprise-architecture-agent.md` | Codex, documentation skill, security review when risk is present | TAP Lite, architecture standards, governance docs, platform runbooks | TAP Lite completeness, risk register quality, ADR traceability, executive summary quality |
| AAP Platform Copilot | oMLX reasoning or coding | `docs/agents/aap-platform-agent.md` | Codex, enterprise automation skill, playbook review tools when available | AAP standards, playbooks, upgrade guides, governance, ROI assumptions | Recommendation usefulness, playbook review accuracy, upgrade guidance, ROI math |
| Satellite Platform Copilot | oMLX reasoning | `docs/agents/satellite-platform-agent.md` | Codex, devops skill, security skill for compliance work | Satellite lifecycle policy, content views, patch windows, compliance requirements | Lifecycle correctness, compliance mapping, upgrade sequencing, governance fit |
| Server Engineering Copilot | oMLX reasoning or coding | `docs/agents/server-engineering-agent.md` | Codex, devops skill, shell validation where safe | Runbooks, incident notes, logs, monitoring reports, DR docs | RCA evidence quality, remediation safety, rollback clarity, runbook readiness |
| Executive Communications Copilot | oMLX reasoning for synthesis, E4B for drafts | `docs/agents/executive-briefing-agent.md` | Codex, documentation skill, source-domain agent handoffs | Quarterly reviews, monthly updates, Summit notes, operational and architecture evidence | Executive clarity, fact/assumption separation, decision asks, measurable outcomes |
| Automation Discovery Copilot | oMLX reasoning, E2B for routing | `docs/agents/automation-discovery-agent.md` | Codex, enterprise automation skill, source ticket or workflow exports | Manual work inventories, service owner notes, process maps, AAP knowledge base | Candidate quality, effort/savings estimate, implementation path, owner handoff |
| Operational Review Copilot | oMLX reasoning, E4B for summaries | `docs/agents/operational-review-agent.md` | Codex, platform reports, benchmark and drift docs | Health monitoring, drift detection, capacity, DR, SLOs, benchmark trends | KPI coverage, exception handling, trend quality, leadership actionability |

## Execution Pattern

1. Select the agent from `docs/agents/agent-catalog.md`.
2. Attach the smallest source evidence set that can support the requested business output.
3. Load the relevant knowledge base from `docs/knowledge/`.
4. Use the prompt contract in the agent document and the standard catalog header.
5. Record runtime lane, source evidence, output artifact, validation result, and owner handoff.
6. Run the appropriate evaluation rubric from `docs/agents/agent-evaluation-framework.md`.
7. Capture measurable business value using `docs/agents/business-value-framework.md`.

## Operational Backlog

| Priority | Work item | Output | Business value measure |
|---|---|---|---|
| 1 | Enterprise Architecture Copilot TAP Lite run | TAP Lite package and ADR candidate | Architecture effort reduced, review cycle shortened |
| 1 | Executive Communications Copilot monthly update | Leadership update from operational evidence | Reporting effort reduced, decision latency reduced |
| 1 | Automation Discovery Copilot backlog sweep | Ranked automation opportunities | Opportunities found, estimated hours saved |
| 2 | AAP Platform Copilot playbook review | Review notes and remediation path | Review effort reduced, automation quality improved |
| 2 | Satellite Platform Copilot lifecycle review | Patch and content-view guidance | Compliance risk reduced, upgrade planning improved |
| 2 | Operational Review Copilot monthly review | KPI and exception report | Operational efficiency and incident prevention |
| 3 | Server Engineering Copilot runbook refinement | Updated runbook or RCA | Recovery time reduced, repeat work eliminated |

## Run Record Template

```text
Agent:
Date:
Runtime lane:
Source evidence:
Knowledge base:
Output artifact:
Evaluation score:
Business value metric:
Owner:
Next action:
Open risks:
```

## Validation

Operationalization is valid when every agent has a prompt contract, runtime lane, required knowledge source, MCP or tool dependency notes, evaluation rubric, memory handling rules, owner handoff, and measurable value metric.
