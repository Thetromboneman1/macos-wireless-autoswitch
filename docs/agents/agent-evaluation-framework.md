# Agent Evaluation Framework

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

This framework evaluates operational agent outputs for accuracy, completeness, consistency, usefulness, executive quality, and governance compliance.

## Evaluation Dimensions

| Dimension | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| Accuracy | Claims conflict with evidence | Mostly correct with minor unsupported statements | Claims are evidence-backed and assumptions are labeled |
| Completeness | Missing required sections or owner actions | Covers core sections with some gaps | Covers required sections, decisions, risks, validation, and handoff |
| Consistency | Conflicts with runtime, governance, or knowledge docs | Minor terminology or structure drift | Aligns with catalog, runtime, knowledge, and governance docs |
| Usefulness | Not actionable | Useful but needs owner refinement | Owner can use it directly for the stated workflow |
| Executive quality | Too technical or vague for leadership | Clear but missing decision framing | Concise, outcome-focused, decision-ready |
| Governance compliance | Exposes or requests unsafe data, ignores controls | Controls mentioned but incomplete | Follows secret, approval, audit, and evidence rules |

## Minimum Passing Bar

| Output type | Minimum |
|---|---|
| Architecture or TAP Lite | 24 of 30 and no governance score below 4 |
| Playbook or operations review | 22 of 30 and no accuracy score below 4 |
| Executive communication | 24 of 30 and executive quality score of 5 |
| Automation discovery | 22 of 30 and usefulness score of 4 or higher |

## Reusable Evaluation Harness

Use this prompt after every material agent output:

```text
Evaluate this agent output against docs/agents/agent-evaluation-framework.md.

Agent:
Output type:
Source evidence:
Output:

Return:
1. Scores for accuracy, completeness, consistency, usefulness, executive quality, and governance compliance.
2. Evidence-backed findings.
3. Required fixes before owner handoff.
4. Final pass/fail.
```

## Regression Fixtures

Continuous tests in `tests/agents/` verify that required operational docs exist and contain the core contracts. Sample-run regression should use sanitized artifacts only and must not include credentials, private tokens, or raw incident data.

## Human Review

Human owners review outputs before external distribution, production changes, governance approval, or executive publication. Agent evaluation is a quality gate, not delegated authority.
