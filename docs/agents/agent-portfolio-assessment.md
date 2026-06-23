# Agent Portfolio Assessment

Date: 2026-06-23
Owner: AI Workforce Program

## Purpose

This assessment moves the local AI platform from platform maturity into business-value delivery. The current platform already provides Codex, OpenCode, Goose, Hermes, OpenClaw, oMLX, llama.cpp, Rapid-MLX, MCP integrations, health monitoring, drift detection, AIOps, governance, documentation, and benchmarks. The next useful work is an enterprise agent portfolio for daily infrastructure, architecture, automation, governance, and executive communication.

## Current Platform Baseline

| Capability | Evidence | Assessment |
|---|---|---|
| Production model lane | `config/local-ai-platform/routing-policy.json` and `docs/architecture/model-routing.md` | Ready for agent execution through oMLX at `http://127.0.0.1:18080/v1`. |
| Model roles | Gemma 31B reasoning, 26B A4B coding, E4B fast-agent, E2B routing/utility | Ready. Preserve the role contract across all agents. |
| Reliability lane | llama.cpp at `http://127.0.0.1:8002/v1` | Ready for measured GGUF coding and reliability validation, not default agent routing. |
| Experimental lane | Rapid-MLX at `http://127.0.0.1:8010/v1` | Lab only. Use for controlled trials, not production agent defaults. |
| MCP topology | `config/local-ai-platform/mcp-topology.json` and `docs/architecture/mcp-topology.md` | Ready for knowledge, repo, and tool integrations. |
| Skills | `~/.agents/skills`, `docs/skills/shared-skills-library.md` | Ready. Enterprise automation skill is the nearest existing domain skill. |
| Operations | `docs/operations/platform-operations-center.md` | Ready for monthly, quarterly, and incident review workflows. |
| Governance | `docs/governance/platform-audit-framework.md` and documentation governance docs | Ready for agent output review and operating controls. |

## Existing Agents

| Agent or surface | Current role | Reuse decision |
|---|---|---|
| Codex | Primary autonomous maintainer and repo/documentation worker | Use for agent authoring, reviews, sample runs, validation, and controlled repo updates. |
| OpenCode | Local coding shell with oMLX and GGUF providers | Use for interactive engineering and playbook/repo review. |
| Goose | Installed agent client | Use for operator-facing guided workflows after prompt contracts are stable. |
| Hermes | Agent/workbench consumer | Use for reusable copilot workflows and tool-call validation. |
| OpenClaw | Agent/workbench consumer | Use for broader agent execution only with Boneman-backed secrets and existing gateway controls. |
| llm-wiki | Local knowledge layer | Use for session memory and promoted platform knowledge. |
| Understand-Anything skills | Repo analysis skills | Use for deep codebase/domain understanding when a copilot needs repository context. |

## Partially Implemented Agents

| Capability | Current evidence | Gap |
|---|---|---|
| Platform Operations Center | `docs/operations/platform-operations-center.md` and AIOps cycle scripts | Needs an Operational Review Copilot contract for monthly/quarterly review synthesis. |
| Documentation governance | Documentation review policy and scripts | Needs agent-facing prompts that convert findings into executive and owner actions. |
| Benchmark governance | Benchmark governance docs/scripts | Needs agent-facing routing decisions and business interpretation. |
| Enterprise automation support | Shared `enterprise-automation` skill | Needs dedicated AAP, Satellite, Server Engineering, and Automation Discovery copilots. |
| Executive reporting | `docs/executive/ai-platform-executive-summary.md` | Needs a reusable Executive Communications Copilot. |

## Overlapping Agents

| Overlap | Risk | Portfolio decision |
|---|---|---|
| AAP Platform Copilot and Automation Discovery Copilot | Both identify automation opportunities | Discovery owns intake and business case; AAP owns implementation governance and platform adoption. |
| Enterprise Architecture Copilot and Operational Review Copilot | Both summarize risk and decisions | Architecture owns design-time review and ADRs; Operational Review owns runtime performance, KPIs, and recurring governance evidence. |
| Executive Communications Copilot and all domain copilots | Every agent can produce summaries | Domain agents produce facts and recommendations; Executive Communications converts them into CIO, board, and quarterly narratives. |
| Server Engineering Copilot and Satellite Platform Copilot | Both touch patching and incidents | Satellite owns content, lifecycle, and compliance; Server Engineering owns OS troubleshooting and incident remediation. |

## Missing Agents

| Missing agent | Business value | Priority |
|---|---|---|
| Enterprise Architecture Copilot | Faster TAP Lite packages, architecture reviews, decision records, and risk summaries | Phase 2 |
| AAP Platform Copilot | Better automation intake, playbook quality, ROI, upgrade planning, and adoption reporting | Phase 3 |
| Satellite Platform Copilot | Patch planning, lifecycle compliance, content governance, and capacity review | Phase 4 |
| Server Engineering Copilot | Faster incident response, root cause analysis, remediation guidance, and runbooks | Phase 5 |
| Executive Communications Copilot | CIO-ready updates, board summaries, risk narratives, and quarterly reviews | Phase 6 |
| Automation Discovery Copilot | Finds manual work, estimates savings, and recommends implementation paths | Phase 7 |
| Operational Review Copilot | Monthly/quarterly platform health, KPI, drift, governance, and benchmark reviews | Phase 8 |

## Portfolio Operating Model

| Role | Primary model lane | Why |
|---|---|---|
| Complex architecture, risk, and governance synthesis | Gemma 31B reasoning on oMLX | Best fit for broad reasoning and review synthesis. |
| Drafting playbooks, runbooks, prompts, and documentation | Gemma 26B A4B coding on oMLX | Default local production coding and structured writing lane. |
| Short summaries, classification, and routing | Gemma E4B or E2B on oMLX | Lower-cost utility work without changing the architecture. |
| Deterministic coding/reliability comparison | llama.cpp GGUF lane | Use only when measured GGUF behavior is specifically required. |
| Experimental tool-call trials | Rapid-MLX lab lane | Manual trial only. Do not promote without benchmark and governance evidence. |

## Validation Summary

Each agent must pass:

- prompt quality: role, audience, inputs, constraints, output schema, and review checklist are explicit;
- output quality: sample runs produce directly usable work products;
- documentation quality: purpose, workflow, dependencies, ownership, and maintenance are documented;
- integration path: Codex, VS Code, Hermes, OpenCode, and shared skills usage are defined;
- operational workflow: owner handoff, evidence collection, validation, and cadence are described.

## Recommendation

Create the seven enterprise copilots as reusable prompt contracts, not new platform services. Keep the platform front door unchanged: oMLX production lane first, llama.cpp only for measured reliability/coding cases, Rapid-MLX as a lab lane, and secrets in Boneman.
