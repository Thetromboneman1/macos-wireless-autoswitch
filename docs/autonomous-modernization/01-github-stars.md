# 01 - GitHub Stars

Raw export: `github-stars.json`

Ranked export: `github-stars-ranked.json`

## Decision Rules

| Category | Meaning | Default action |
| --- | --- | --- |
| Must Implement | Directly relevant to local AI, agent workflows, Apple Silicon, or current repos | Integrate or document if it improves the actual stack |
| High Value | Strong candidate but needs a separate workflow target | Evaluate and document |
| Nice To Have | Useful but not central to local AI/DNS/repo automation | Document only |
| Research Only | Interesting, broad, or unrelated to current stack | Ignore unless needed |
| Obsolete | Archived or replaced | Ignore |

## Star Review Summary

| Repo | Category | Action | Why |
| --- | --- | --- | --- |
| `kennss/SiliconScope` | Must Implement | Document/evaluate | Apple Silicon telemetry could improve benchmark visibility. |
| `Egonex-AI/Understand-Anything` | Must Implement | Defer install | Code graph value is high, but needs a target repo and indexing budget. |
| `garrytan/gbrain` | Must Implement | Research only | Overlaps OpenClaw/Hermes; no install without conflict review. |
| `nvk/llm-wiki` | Must Implement | Document/evaluate | Strong fit for Codex/OpenCode knowledge-base workflows. |
| `john-rocky/coreai-model-zoo` | Must Implement | Defer | Prior compatibility check says macOS/Xcode runtime floor is not current production fit. |
| `affaan-m/ECC` | Must Implement | Research only | Agent methodology overlap; no install until trust and scope review. |
| `aaif-goose/goose` | Must Implement | Keep documented | Existing Goose config is part of the local stack. |
| `google-gemma/gemma-skills` | Must Implement | Document/evaluate | Relevant to Gemma tool-use behavior. |
| `osaurus-ai/osaurus` | Must Implement | Defer | Native macOS agent harness, but overlaps current agent stack. |
| `Thetromboneman1/hermes-*` / `NousResearch/hermes-agent` | Must Implement | Keep aligned | Existing repos already carry Hermes integration. |
| `Thetromboneman1/Openclaw` | Must Implement | Keep aligned | Existing local-AI Docker/OpenCode repo. |
| `diegosouzapw/OmniRoute` | Must Implement | Defer changes | Powerful but duplicates local gateway paths; current checkout is clean. |
| `ApodexAI/AgentHarness` | High Value | Defer | Useful eval harness, but no Apodex serving target selected. |
| `StarTrail-org/LEANN` | High Value | Defer | Private RAG value, requires corpus/indexing plan. |
| `headroomlabs-ai/headroom` | High Value | Defer | Token compression may help later, but proxy/MCP layer adds complexity. |
| `OpenHands/OpenHands` | High Value | Ignore for now | Full agent platform duplicates Codex/OpenCode/Hermes. |
| `apple/container` | High Value | Document | Useful Mac container tech, but not a model-serving replacement. |
| `NPC-Worldwide/npcsh` | High Value | Defer | Agent shell candidate; needs isolated trial. |
| Other stars | Nice To Have / Research Only | Document or ignore | No immediate improvement to DNS/local-AI/agent workflow. |

## Rollback

No starred repo was installed or vendored in this pass, so rollback is documentation-only.

