# Agent Catalog

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

This catalog is the reusable entry point for the enterprise AI workforce. Each agent is a prompt contract plus an operating workflow that uses the existing local AI platform.

## Catalog

| Agent | Purpose | Primary audience | Default model lane | Documentation |
|---|---|---|---|---|
| Enterprise Architecture Copilot | TAP Lite, architecture review, risk, ADRs, governance, executive summaries | Enterprise Architecture and platform leaders | oMLX 31B reasoning | `docs/agents/enterprise-architecture-agent.md` |
| AAP Platform Copilot | AAP opportunity, playbook review, governance, ROI, upgrade, migration, adoption, reporting | AAP platform owner and automation engineers | oMLX 31B or 26B | `docs/agents/aap-platform-agent.md` |
| Satellite Platform Copilot | Patch planning, content view, lifecycle, compliance, upgrade, capacity, governance | Satellite platform owner and Linux leadership | oMLX 31B | `docs/agents/satellite-platform-agent.md` |
| Server Engineering Copilot | Linux/Windows troubleshooting, log analysis, RCA, remediation, runbooks, incidents | Server engineering and operations | oMLX 31B or 26B | `docs/agents/server-engineering-agent.md` |
| Executive Communications Copilot | CIO updates, board summaries, project status, risks, summit takeaways, quarterly reviews | Executives and sponsors | oMLX 31B or E4B | `docs/agents/executive-briefing-agent.md` |
| Automation Discovery Copilot | Manual work discovery, automation candidates, effort, savings, implementation path | Automation strategy and service owners | oMLX 31B or E2B | `docs/agents/automation-discovery-agent.md` |
| Operational Review Copilot | Monthly/quarterly reviews, KPIs, health, governance reporting | Platform operations and leadership | oMLX 31B or E4B | `docs/agents/operational-review-agent.md` |

## Standard Prompt Header

Use this header before the agent-specific prompt contract:

```text
Use the enterprise agent catalog.
Selected agent: <agent name>.
Audience: <audience>.
Decision or outcome needed: <outcome>.
Source evidence: <files, notes, logs, exports, or reports>.
Constraints: preserve oMLX-first routing, do not expose secrets, distinguish facts from assumptions.
Expected artifact: <artifact type>.
```

## Dependencies

| Dependency | Use |
|---|---|
| `docs/agents/operationalization-plan.md` | Operational run pattern, runtime mapping, tool dependencies, and validation strategy for every copilot. |
| `docs/agents/agent-evaluation-framework.md` | Reusable scoring rubric for operational agent outputs. |
| `docs/agents/agent-memory-architecture.md` | Short-term, project, knowledge, evaluation, and business value memory rules. |
| `docs/agents/agent-orchestration.md` | Handoffs between agents for daily, weekly, monthly, quarterly, and event-driven workflows. |
| `docs/agents/business-value-framework.md` | Measurement model for time saved, opportunities found, reporting effort reduced, and operational efficiency. |
| `docs/knowledge/` | Domain knowledge-base definitions for TAP Lite, AAP, Satellite, enterprise knowledge, and Red Hat Summit workflows. |
| `config/local-ai-platform/routing-policy.json` | Model lane and endpoint source of truth. |
| `config/local-ai-platform/mcp-topology.json` | Tool and knowledge integration source of truth. |
| `docs/architecture/model-routing.md` | Human-readable model lane policy. |
| `docs/architecture/mcp-topology.md` | Human-readable MCP and client topology. |
| `docs/skills/shared-skills-library.md` | Shared skill routing and maintenance. |
| `docs/operations/platform-operations-center.md` | Operational review and AIOps workflow. |
| Boneman vault | Secret storage and credential pointers. |

## Ownership

| Agent | Owner | Maintenance cadence |
|---|---|---|
| Enterprise Architecture Copilot | Enterprise Architecture | Quarterly or after standards changes. |
| AAP Platform Copilot | AAP Platform Owner | Monthly and after AAP upgrades. |
| Satellite Platform Copilot | Satellite Platform Owner | Monthly patch cycle and before upgrades. |
| Server Engineering Copilot | Server Engineering | After major incidents and runbook updates. |
| Executive Communications Copilot | Executive Communications | Quarterly or after leadership format changes. |
| Automation Discovery Copilot | Automation Strategy | Monthly backlog review. |
| Operational Review Copilot | Platform Operations | Monthly operations cycle. |

## Maintenance Process

1. Update the relevant agent file.
2. Confirm the prompt contract still includes role, inputs, rules, and output schema.
3. Confirm runtime mapping still matches `config/local-ai-platform/routing-policy.json`.
4. Confirm the operationalization plan still names runtime, prompts, tools, MCP dependencies, required knowledge, and validation strategy.
5. Run documentation and agent regression validation.
6. Capture a sample run in the agent file or in a linked operating artifact.
7. Record measurable value when the run supports a daily workflow.
8. Commit the change with the related agent or catalog update.

## Sample Agent Selection

| Request | Select agent | Reason |
|---|---|---|
| "Create a TAP Lite for expanding AAP automation." | Enterprise Architecture Copilot | Architecture decision package is the primary output. |
| "Review this playbook and estimate value." | AAP Platform Copilot | Playbook quality and ROI belong to AAP ownership. |
| "Build next month's patch plan." | Satellite Platform Copilot | Satellite content and lifecycle state drive the plan. |
| "Summarize this outage for leadership." | Server Engineering Copilot, then Executive Communications Copilot | Technical RCA first, executive packaging second. |
| "Find automation candidates in these tickets." | Automation Discovery Copilot | Candidate discovery and ranking is the first step. |
| "Generate the quarterly platform review." | Operational Review Copilot, then Executive Communications Copilot | Evidence review first, leadership narrative second. |

## Validation

The catalog is valid when every listed agent has:

- a purpose and audience;
- documented capabilities;
- a prompt contract;
- dependencies and runtime integration;
- owner and maintenance cadence;
- validation checklist;
- at least one sample run;
- an operationalization entry;
- an evaluation rubric;
- a knowledge source;
- an orchestration path;
- a business value metric.
