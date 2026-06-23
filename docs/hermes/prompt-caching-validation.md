# Hermes Prompt Caching Validation

Date: 2026-06-23
Owner: Platform Operations

## Current Result

The local oMLX tiny-chat health check reported:

| Metric | Value |
|---|---:|
| Prompt tokens | 18 |
| Completion tokens | 1 |
| Cached input tokens | 0 |

This is expected for the local OpenAI-compatible lane. No Anthropic cache TTL change was made because Anthropic was not configured or used in this pass.

## Rule

Do not configure provider-specific cache keys unless the installed Hermes version and that provider support them. "Caching supported" is not the same as observed cache hits.

## Evidence

- `docs/autonomous-modernization/evidence/hermes-token-optimization/local-ai-health-chat-baseline.json`
- `docs/autonomous-modernization/evidence/hermes-token-optimization/hermes-cost-baseline.json`
