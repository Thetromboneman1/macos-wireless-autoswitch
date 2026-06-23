# Agent Orchestration

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

Agent orchestration defines handoffs between operational agents so daily workflows produce usable artifacts, owner actions, and measurable business value.

## Orchestration Rules

- Start with the agent that owns the source evidence.
- Handoff only the evidence, findings, decisions, risks, and owner actions needed by the next agent.
- Record runtime lane, sources, validation result, and open risks.
- Do not create new orchestration services; use Codex, Hermes, OpenCode, Goose, or OpenClaw as existing execution surfaces.

## Standard Handoff Record

```text
From agent:
To agent:
Business objective:
Source evidence:
Findings:
Decisions needed:
Risks:
Recommended next action:
Evaluation result:
Business value metric:
```

## Workflows

| Workflow | Sequence | Output |
|---|---|---|
| Automation opportunity to executive ask | Automation Discovery Copilot -> Enterprise Architecture Copilot -> Executive Communications Copilot | Ranked opportunity, TAP Lite or ADR, leadership decision brief |
| Server issue to operational review | Server Engineering Copilot -> Operational Review Copilot | RCA, remediation status, KPI impact, owner actions |
| AAP value reporting | AAP Platform Copilot -> Executive Communications Copilot | Automation status, ROI estimate, executive update |
| Satellite lifecycle governance | Satellite Platform Copilot -> Operational Review Copilot -> Executive Communications Copilot | Lifecycle review, governance exceptions, leadership summary |
| Quarterly platform review | Operational Review Copilot -> Enterprise Architecture Copilot -> Executive Communications Copilot | KPI review, architecture implications, quarterly narrative |

## Daily Workflow Integration

| Cadence | Trigger | Agent sequence | Artifact |
|---|---|---|---|
| Daily | Incident, drift, health exception | Server Engineering or Operational Review | Remediation note or status update |
| Weekly | Manual work or backlog review | Automation Discovery then AAP | Ranked backlog and automation path |
| Monthly | Operations review | Operational Review then Executive Communications | Monthly update |
| Quarterly | Strategy or sponsor review | Enterprise Architecture then Executive Communications | TAP Lite, ADR, quarterly review |
| Event-driven | Red Hat Summit or vendor announcement | Red Hat Summit Assistant then Enterprise Architecture or Executive Communications | Implication brief |

## Validation

Orchestration is valid when each handoff preserves evidence, names the receiving owner, includes a business objective, and produces an artifact that passes the evaluation framework.
