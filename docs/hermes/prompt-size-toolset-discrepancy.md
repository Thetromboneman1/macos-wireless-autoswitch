# Hermes Prompt-Size Toolset Discrepancy

Date: 2026-06-23

## Summary

`hermes tools list --platform cli` confirms the high-cost toolsets are disabled, but `hermes prompt-size --json` still reports 29 tools and about 20,130 estimated tokens. Treat `prompt-size` as a reported/static prompt-budget estimate, not proof of realized per-request token usage.

## Commands

```bash
hermes --version
hermes tools list --platform cli
hermes prompt-size --json
```

Observed version: `Hermes Agent v0.16.0 (2026.6.5)`, upstream `5ecf3bf0`.

## Enabled Runtime Toolsets

Enabled built-ins observed: `web`, `terminal`, `file`, `code_execution`, `skills`, `todo`, `memory`, `session_search`, `clarify`, `delegation`.

Disabled built-ins observed: `browser`, `vision`, `video`, `image_gen`, `video_gen`, `x_search`, `moa`, `tts`, `context_engine`, `cronjob`, `messaging`, `homeassistant`, `spotify`, `yuanbao`, `computer_use`.

MCP server observed: `octopoda`.

## Reported Prompt-Size Output

`hermes prompt-size --json` reported:

| Field | Value |
|---|---:|
| tools.count | 29 |
| tools.json_bytes | 46,774 |
| estimated total tokens | about 20,130 |

## Root Cause

Current evidence points to `prompt-size` measuring the static installed/catalog prompt budget rather than the active enabled-toolset list. The CLI and runtime tool list read the active toolset trim correctly, so the trim should not be reversed to make this metric move.

## Fix Applied

`scripts/operations/hermes-cost-report.py` now labels prompt-size data as reported/static overhead and separately records runtime toolsets parsed from `hermes tools list --platform cli`. `scripts/operations/run-aiops-cycle.sh` captures both files.

## Impact

Cost reports can compare:

- reported theoretical prompt overhead;
- enabled runtime toolsets;
- observed usage records from sessions or endpoint responses.

Do not claim token savings from the static 20,130-token estimate until Hermes exposes request-level realized prompt/tool-schema accounting or upstream clarifies the command behavior.
