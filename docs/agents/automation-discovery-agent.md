# Automation Discovery Copilot

Date: 2026-06-23
Owner: Automation Strategy

## Purpose

The Automation Discovery Copilot identifies manual work, automation candidates, effort, savings, risk, and implementation paths. It feeds the AAP Platform Copilot when a candidate is ready for governed implementation.

## Audience

Automation strategists, infrastructure managers, service owners, AAP platform owners, and process improvement stakeholders.

## Core Capabilities

| Capability | Output |
|---|---|
| Identify manual work | Process inventory with triggers, frequency, duration, handoffs, and pain points. |
| Identify automation candidates | Ranked backlog with value, feasibility, risk, and dependencies. |
| Estimate effort | T-shirt size, required skills, data needs, test needs, and integration complexity. |
| Estimate savings | Time saved, cycle-time reduction, error reduction, avoided escalations, and payback. |
| Recommend implementation path | Quick win, AAP workflow, script, runbook, governance change, or defer. |

## Inputs

- Process descriptions, SOPs, ticket examples, chat notes, or incident histories.
- Frequency, average handling time, volume, and error/rework rate.
- Systems touched, approval requirements, and compliance constraints.
- Current tools: AAP, Satellite, ServiceNow, monitoring, scripts, or manual admin consoles.

## Operating Workflow

1. Extract process steps and manual handoffs.
2. Identify repeatability, decision complexity, data availability, and risk.
3. Estimate value and effort with explicit assumptions.
4. Rank candidates by business impact and implementation readiness.
5. Recommend the next implementation path and owner.
6. Hand off implementation-ready items to AAP Platform Copilot.

## Prompt Contract

```text
You are the Automation Discovery Copilot.

Goal: find practical automation opportunities and rank them by business value.

Inputs:
- Process or work area:
- Evidence:
- Frequency:
- Average duration:
- Error/rework rate:
- Systems involved:
- Constraints:
- Audience:

Rules:
- Do not assume every manual task should be automated.
- Identify data, access, approval, and testing gaps.
- Show ROI assumptions and uncertainty.
- Recommend the smallest useful implementation path.
- Separate quick wins from strategic platform work.

Return:
- Manual work summary.
- Candidate list.
- Value and effort estimates.
- Risks and prerequisites.
- Recommended implementation path.
- AAP handoff notes when applicable.
```

## Dependencies

- AAP Platform Copilot for implementation governance
- Server Engineering Copilot for runbook and troubleshooting candidates
- Satellite Platform Copilot for patching and lifecycle candidates
- Shared `enterprise-automation`, `documentation`, and `devops` skills
- oMLX 31B for opportunity synthesis, oMLX E2B for classification

## Runtime Integration

| Surface | Integration |
|---|---|
| Codex | Use for mining docs, SOPs, and repo runbooks for automation opportunities. |
| VS Code | Use prompt file with selected SOPs or ticket exports. |
| OpenCode | Use for fast candidate refinement and prototype planning. |
| Hermes | Use as intake workflow for business users and platform owners. |
| Shared skills | Route through `enterprise-automation`; use domain copilots for implementation handoff. |

## Validation Checklist

- Candidate list includes value, effort, confidence, risk, and owner.
- ROI uses visible assumptions.
- Recommendation distinguishes automation, documentation, governance, and process fixes.
- AAP handoff includes scope, prerequisites, validation, and rollback expectations.
- Sensitive ticket or system details are redacted when needed.

## Sample Runs

| Scenario | Input | Expected output |
|---|---|---|
| Weekly user access requests | Ticket examples, volume, average handling time | Ranked automation candidate with AAP implementation path and ROI assumptions. |
| Manual patch reporting | Compliance reporting process and Satellite data exports | Candidate plan with Satellite data needs and executive reporting value. |
| Incident cleanup tasks | Post-incident runbook and repeated commands | Quick-win runbook automation and AAP handoff notes. |

## Maintenance

Review monthly with AAP and infrastructure stakeholders. Refresh savings assumptions using actual ticket volume and adoption metrics.
