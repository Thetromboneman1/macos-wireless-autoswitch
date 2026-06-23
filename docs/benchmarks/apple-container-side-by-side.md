# Apple Container Side-By-Side Benchmarks

Date: 2026-06-23

The first workload comparison was run for `ntfy`.

## Baseline Captured

| Runtime | Current state |
|---|---|
| Docker Desktop | production services running |
| Apple Container | 1.0.0 service running, `ac-ntfy` enabled |
| oMLX | healthy on `127.0.0.1:18080` |
| llama.cpp | listening on `127.0.0.1:8002` |
| Rapid-MLX | stopped |

## ntfy Health Latency

| Runtime | Endpoint | Result | Seconds |
|---|---|---|---:|
| Docker Desktop | `http://127.0.0.1:8091/v1/health` | pass | 0.004340 |
| Apple Container | `http://127.0.0.1:19091/v1/health` | pass | 0.005419 |

Raw evidence was written to `/tmp/ac-compare-ntfy.json` during the run.

## Benchmark Plan

For each translated workload, compare Docker Desktop production and Apple Container pilot on startup time, health latency, request latency, CPU, RSS, swap, disk growth, shutdown time, and recovery time. Native AI inference benchmarks stay separate because oMLX/llama/Rapid-MLX are not being containerized.
