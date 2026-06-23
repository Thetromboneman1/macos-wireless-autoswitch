# Long Duration Stability

Date: 2026-06-23

## Purpose

Short benchmarks prove endpoint shape and warm throughput. They do not prove that a lane survives long sessions, swap pressure, cache growth, or repeated tool calls. Long-duration tests are required before any lab lane becomes production.

## Test Tiers

| Tier | Duration | Use |
|---|---:|---|
| Smoke soak | 1 hour | Required after config changes and before daily use. |
| Workday soak | 4 hours | Required before promoting a backend or model. |
| Overnight soak | 8+ hours | Required before always-on production service changes. |

## Metrics

Capture at start, every 5 minutes, and end:

- endpoint health;
- TTFT;
- output tok/s;
- RSS;
- macOS memory pressure;
- swap used;
- process restarts;
- non-2xx responses;
- Hermes one-shot result;
- tool-call result.

## Command Pattern

```bash
scripts/health/local-ai-health.py --json docs/benchmarks/health-snapshot.json
```

For a soak, run a loop from `tmux`:

```bash
while true; do
  scripts/health/local-ai-health.py --json docs/benchmarks/health-snapshot.json || true
  sleep 300
done
```

## Promotion Rule

A lane is promotable only when:

- health checks stay green for the selected tier;
- swap does not grow materially;
- TTFT does not drift upward by more than 25 percent after warmup;
- no process crash or reload loop is observed;
- Hermes passes if Hermes will use the lane.
