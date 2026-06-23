# Platform Disaster Recovery Plan

Date: 2026-06-23
Owner: Platform Operations

## Recovery Objectives

| Scenario | RTO | RPO |
|---|---|---|
| Repository loss | 30 minutes after GitHub access | last pushed commit |
| Documentation loss | 30 minutes after GitHub access | last pushed commit |
| oMLX service unavailable | one active work session | latest local oMLX settings and model cache |
| Model cache loss | one maintenance window | latest downloadable or cached model source |
| LaunchAgent loss | one active work session | latest documented plist/source path |
| OnePassword access unavailable | blocked until vault access restored | last valid Boneman vault state |

## Recovery Workflow

1. Recover repository from `origin/main`.
2. Run `uvx pytest`, `markdownlint` on changed docs, and `git diff --check`.
3. Restore oMLX app/service and verify `http://127.0.0.1:18080/health`.
4. Verify authenticated `/v1/models` returns the Gemma role models.
5. Restore `com.corn.omlx-power-policy` only after checking plist path and logs.
6. Keep llama.cpp and Rapid-MLX stopped until production oMLX is healthy.
7. Restore Docker consumers to `host.docker.internal:18080/v1` only after host endpoint validation.
8. Restore secret values from Boneman or local secure stores; never paste raw values into Git.
9. Run health, drift, documentation, and AIOps cycle.

## Recovery Boundaries

- Production first: oMLX on `18080`.
- Lab lanes second: llama.cpp `8002`, Rapid-MLX `8010`.
- Tooling last: VS Code extensions, Codex skills, optional Docker companions.

## Validation Commands

```bash
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health-dr.json
scripts/health/drift-detection/check-platform-drift.py --health-json /tmp/local-ai-health-dr.json --json /tmp/platform-drift-dr.json
scripts/operations/run-aiops-cycle.sh
```
