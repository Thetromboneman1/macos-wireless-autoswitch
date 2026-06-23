# Hermes Budget Controls

Date: 2026-06-23
Owner: Platform Operations

## Current State

No new paid cloud provider was configured. The active default is local oMLX, so routine inference has no API bill.

## Required Controls Before Cloud Use

| Control | Requirement |
|---|---|
| Credential storage | 1Password vault `Boneman`. |
| Provider dashboard | Enable spend alert or hard cap where supported. |
| Fallback loops | Set bounded retries; no automatic multi-provider loop without approval. |
| Delegation | Keep max depth and child count bounded. |
| Tool loops | Keep max tool-call limits enabled. |
| Reporting | Run `scripts/operations/hermes-cost-report.py` and AIOps cycle. |

## Weekly Review

Review:

- actual model used versus configured default;
- cache-hit percentage;
- input/output split;
- fallback events;
- background costs;
- high-cost sessions;
- local-versus-cloud percentage.
