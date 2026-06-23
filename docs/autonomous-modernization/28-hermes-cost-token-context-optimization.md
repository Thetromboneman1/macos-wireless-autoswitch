# 28 - Hermes Cost Token Context Optimization

Date: 2026-06-23
Owner: Platform Operations

## Executive Summary

This pass audited the Reddit cost/token PDF against the installed Hermes CLI, preserved the oMLX-first architecture, trimmed high-cost default CLI tool availability, added token/cost observability to AIOps, and documented the guardrails for compression, memory, cloud fallback, browser use, and background jobs.

No cloud provider was added. No paid service was configured. No memory was deleted. Gemma was not demoted because local validation still passes.

## Baseline

| Metric | Value |
|---|---:|
| Fixed prompt estimate | 20,130 tokens |
| Tool-schema estimate | 11,694 tokens |
| Skills-index estimate | 2,788 tokens |
| Memory estimate | 38 tokens |
| User-profile estimate | 40 tokens |
| oMLX tiny chat | pass |
| Optional llama.cpp | stopped/manual |
| Optional Rapid-MLX | stopped/manual |
| Swap pressure | high |

## Changes Implemented

- Captured PDF text and baseline evidence under `docs/autonomous-modernization/evidence/hermes-token-optimization/`.
- Disabled high-cost CLI default toolsets: `browser`, `vision`, `image_gen`, `tts`, `cronjob`, `messaging`, `computer_use`.
- Added `scripts/operations/hermes-cost-report.py`.
- Integrated Hermes cost reporting into `scripts/operations/run-aiops-cycle.sh` and `scripts/operations/generate-platform-report.py`.
- Added tests for fixed-overhead and usage aggregation.
- Added runbooks for toolsets, prompt compaction, memory hygiene, compression, auxiliary models, caching, browser cost controls, LaunchAgents, background jobs, budget controls, provider privacy, monitoring, and governance.

## Rejected Or Deferred

| Item | Decision |
|---|---|
| Replace oMLX/Gemma with a cloud default | Rejected; local lane is healthy and private. |
| Demote Gemma because of Reddit comments | Rejected; this machine has local validation evidence. |
| Enable DeepSeek/OpenAI/Anthropic fallback | Deferred; requires explicit approval and budget/privacy controls. |
| Install `hermes-tool-router` globally | Deferred; source/security/maintenance review needed. |
| Delete/prune memories | Rejected; built-in memories are already tiny. |
| Lower compression threshold | Rejected; current 0.50 is conservative and already enabled. |
| Add new LaunchAgents | Rejected; no hidden always-on services. |

## Before And After

| Metric | Before | After |
|---|---:|---:|
| High-cost CLI defaults disabled | 0 | 7 |
| `prompt-size` tool count | 29 | 29 |
| Estimated total fixed tokens | 20,130 | 20,130 |
| Estimated tool-schema tokens | 11,694 | 11,694 |
| Hermes one-shot | not captured | pass |

`prompt-size` did not show token savings after tool trimming, so no percentage reduction is claimed.

## Rollback

Config backup path:

```text
docs/autonomous-modernization/evidence/hermes-token-optimization/config-backup-dir.txt
```

Re-enable the disabled CLI toolsets:

```bash
hermes tools enable --platform cli browser vision image_gen tts cronjob messaging computer_use
```

## Validation Evidence

- `uvx pytest tests/test_aiops_operations.py -q` passed.
- `scripts/health/local-ai-health.py --json ...` passed after trim.
- `hermes -z 'Reply with exactly OK.' -t terminal,file,web,skills,memory,todo,clarify ...` returned `OK.`

## Commit And Push Status

| Repository | Commit | Push status |
|---|---|---|
| `macos-wireless-autoswitch` | `58571c0`, `d216b8c` | Pushed to `origin/main`; final HEAD is recorded in the completion response. |

External Hermes user config was changed through the supported `hermes tools disable --platform cli ...` command and backed up before editing. That config lives under `~/.hermes/config.yaml`, outside this repository.

## Remaining Manual Actions

- Run a long-session compression test before changing compression thresholds.
- Run request-level Hermes dumps if exact schema-token reduction is required.
- Review Hermes upstream behavior where `prompt-size` does not reflect platform tool trimming.
- Configure provider-side budget caps only if a cloud provider is explicitly approved.
