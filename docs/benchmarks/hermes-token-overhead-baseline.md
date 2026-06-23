# Hermes Token Overhead Baseline

Date: 2026-06-23
Owner: Platform Operations

## Scope

This baseline uses installed Hermes offline prompt sizing plus local oMLX health probes. It does not claim full request-level token decomposition for every workload because the current Hermes CLI exposes fixed prompt sizing but not every internal bucket for every one-shot request.

## Captured Artifacts

| Artifact | Purpose |
|---|---|
| `docs/autonomous-modernization/evidence/hermes-token-optimization/prompt-size-cli-baseline.json` | Fixed CLI prompt, memory, skills, and tool-schema budget. |
| `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-tools-list-baseline.txt` | Enabled/disabled CLI toolsets before trimming. |
| `docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-baseline.json` | oMLX `/v1/models` plus tiny chat completion. |
| `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-cost-baseline.json` | Machine-readable baseline cost report. |

## Baseline Measurements

| Metric | Value |
|---|---:|
| Model | `mlx-community--gemma-4-26b-a4b-it-4bit` |
| Tool count reported by `prompt-size` | 29 |
| Estimated fixed prompt tokens | 20,130 |
| Estimated tool-schema tokens | 11,694 |
| Estimated skills-index tokens | 2,788 |
| Estimated memory tokens | 38 |
| Estimated user-profile tokens | 40 |
| oMLX tiny-chat prompt tokens | 18 |
| oMLX tiny-chat completion tokens | 1 |
| Cached input tokens | 0 |
| Optional llama.cpp lane | stopped intentionally |
| Optional Rapid-MLX lane | stopped intentionally |
| Swap pressure | high |

## Workload Coverage

| Workload | Status | Evidence |
|---|---|---|
| Minimal greeting | Captured | `local-ai-health-chat-baseline.json` |
| Shell task | Covered by tool availability, not request-level token dump | `prompt-size-cli-baseline.json` |
| Coding task | Covered by current CLI fixed prompt budget | `prompt-size-cli-baseline.json` |
| Multi-tool task | Deferred request-level run | Requires Hermes session dump parsing. |
| Research task | Deferred request-level run | Requires cloud/web workflow decision. |
| Long-session task | Deferred request-level run | Compression validation needed. |
| Subagent task | Deferred | Delegation remains enabled; no child task spawned. |

## Baseline Caveat

`hermes prompt-size --json` reports byte/character budgets. The repository cost report converts them with a four-character token approximation when exact token counts are absent. Use this for trend detection, not billing-grade accounting.
