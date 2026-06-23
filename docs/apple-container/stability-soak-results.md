# Apple Container Stability Soak Results

Date: 2026-06-23

`ac-ntfy` has passed startup, health, restart, and self-heal smoke checks. Longer soak stages remain pending because live swap was already high, about 80 percent used, before the mirror started.

## Planned Stages

| Stage | Duration | Gate |
|---|---:|---|
| Smoke | 5 minutes | startup, health, logs, shutdown |
| Repeated request | 30 minutes | no restart, bounded memory |
| Stability | 1 hour | no production impact |
| Extended | 4 hours | only after 1-hour pass |
| Overnight | 8+ hours | explicit safety review first |

Stop conditions: production port collision, unexpected swap growth, production endpoint degradation, data-root violation, or repeated health failures.

## Completed Smoke Checks

| Check | Result |
|---|---|
| Start `ac-ntfy` | pass |
| Health `http://127.0.0.1:19091/v1/health` | pass |
| Compare Docker and Apple Container ntfy health | pass |
| Restart `ac-ntfy` | pass |
| Stop `ac-ntfy` and self-heal | pass |
| Docker production ntfy after self-heal | pass |
