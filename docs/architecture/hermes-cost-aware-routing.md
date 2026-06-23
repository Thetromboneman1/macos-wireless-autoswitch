# Hermes Cost-Aware Routing

Date: 2026-06-23
Owner: Platform Operations

## Routing Policy

Hermes remains local-first:

1. Use oMLX at `http://127.0.0.1:18080/v1` for ordinary, private, and default work.
2. Keep llama.cpp at `http://127.0.0.1:8002/v1` as a manual GGUF coding/control lane.
3. Keep Rapid-MLX at `http://127.0.0.1:8010/v1` as a manual lab lane.
4. Use cloud providers only after privacy classification and explicit approval.
5. Do not use OpenRouter for single-provider convenience when direct provider access is sufficient.

## Current Evidence

| Check | Result |
|---|---|
| oMLX `/v1/models` | Passed. |
| oMLX tiny chat | Passed. |
| Hermes one-shot after trim | Passed. |
| llama.cpp lane | Intentionally stopped. |
| Rapid-MLX lane | Intentionally stopped. |
| Swap pressure | High; do not add always-on model lanes. |

## Cloud Escalation Rules

Cloud fallback requires all of:

- task is not sensitive, or user approves the data handling risk;
- provider credential is stored in 1Password vault `Boneman`;
- max retry, delegation depth, and tool-loop limits are documented;
- provider dashboard budget alert or cap exists where supported;
- final report records provider, model, reason, and estimated usage.
