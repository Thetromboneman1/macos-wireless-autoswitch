# Apple Container Stability Soak Results

Date: 2026-06-23

No Apple Container workload soak has been run yet. This is intentional: the request requires current-state discovery before migration, and no mirrored workload should start until its Compose translation and isolation plan is complete.

## Planned Stages

| Stage | Duration | Gate |
|---|---:|---|
| Smoke | 5 minutes | startup, health, logs, shutdown |
| Repeated request | 30 minutes | no restart, bounded memory |
| Stability | 1 hour | no production impact |
| Extended | 4 hours | only after 1-hour pass |
| Overnight | 8+ hours | explicit safety review first |

Stop conditions: production port collision, unexpected swap growth, production endpoint degradation, data-root violation, or repeated health failures.
