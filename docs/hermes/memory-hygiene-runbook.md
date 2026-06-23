# Hermes Memory Hygiene Runbook

Date: 2026-06-23
Owner: Platform Operations

## Current State

Built-in Hermes memory is already small:

| File | Bytes | Decision |
|---|---:|---|
| `~/.hermes/memories/MEMORY.md` | 9 | No pruning. |
| `~/.hermes/memories/USER.md` | 15 | No pruning. |

`hermes memory status` was captured in `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-memory-status-baseline.txt`.

## Safe Review Procedure

1. Back up `~/.hermes/memories/`.
2. Export file sizes and checksums.
3. Classify entries as durable preference, operational fact, stale fact, duplicate, sensitive, or temporary.
4. Remove only stale duplicates with clear evidence.
5. Run `hermes prompt-size --json` before and after.
6. Run a tiny local oMLX chat and one Hermes one-shot.

## Prohibited Automation

Do not create unattended deletion of memories. A weekly review may report growth and suspected duplicates, but deletion needs an explicit human decision.
