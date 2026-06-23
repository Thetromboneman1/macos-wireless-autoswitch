---
mode: agent
description: Invoke the enterprise AI workforce copilots using the repo-local agent catalog.
---

# Enterprise Agent Workforce

Use `docs/agents/agent-catalog.md` to select the correct copilot before producing an artifact.

## Available Agents

- `enterprise-architecture`: TAP Lite, architecture review, risk analysis, ADRs, design validation, governance compliance, executive summaries.
- `aap-platform`: automation opportunity discovery, playbook review, automation governance, ROI, upgrade planning, migration planning, adoption tracking, executive reporting.
- `satellite-platform`: patch planning, content view review, lifecycle review, compliance reporting, upgrade planning, capacity review, governance recommendations.
- `server-engineering`: Linux/Windows troubleshooting, log analysis, RCA, remediation guidance, runbook generation, incident summaries.
- `executive-briefing`: CIO updates, executive summaries, board-level summaries, project status updates, risk summaries, summit takeaways, quarterly reviews.
- `automation-discovery`: manual work identification, automation candidate ranking, effort and savings estimates, implementation path.
- `operational-review`: monthly reviews, quarterly reviews, KPI reporting, platform health reviews, governance reporting.

## Runtime Rules

- Preserve oMLX at `http://127.0.0.1:18080/v1` as the default local production lane.
- Preserve the Gemma role contract: 31B reasoning, 26B A4B coding, E4B fast agent, E2B routing/utility.
- Use llama.cpp at `http://127.0.0.1:8002/v1` only for measured GGUF coding or reliability tasks.
- Keep Rapid-MLX at `http://127.0.0.1:8010/v1` as a manual lab lane.
- Do not default to Ollama.
- Do not expose secret values. Refer to Boneman item names or retrieval methods only.

## Invocation Template

```text
Selected agent:
Audience:
Outcome needed:
Source evidence:
Constraints:
Required artifact:
Review standard:
```

## Output Standard

Every agent output must include:

- summary;
- source evidence and missing evidence;
- findings or recommendations;
- risks and assumptions;
- owner actions;
- validation or review checklist;
- executive-ready summary when relevant.

If the request is ambiguous, choose the closest agent from the catalog and state the assumption before producing the artifact.
