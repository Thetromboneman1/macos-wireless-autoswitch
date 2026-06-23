# Hermes Persistent Prompt Optimization

Date: 2026-06-23
Owner: Platform Operations

## Files Reviewed

| File | Words | Bytes | Decision |
|---|---:|---:|---|
| `~/.hermes/SOUL.md` | 109 | 695 | Already compact. |
| `~/.hermes/.hermes/SOUL.md` | 72 | 513 | Already compact. |
| `~/.hermes/memories/USER.md` | 3 | 15 | Empty profile shell; no trim needed. |

## Decision

No persistent prompt file was edited. The source PDF recommends keeping SOUL and USER content near 500 to 1,000 tokens each; this installation is already far below that. Further reduction would risk deleting useful behavior for negligible savings.

## Regression Check

After toolset trimming, Hermes one-shot with a focused toolset still returned `OK`, and local oMLX health remained green.

Evidence:

- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-oneshot-after-trim.txt`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-after-trim.json`
