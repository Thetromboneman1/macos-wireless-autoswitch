# Apple Container Side-By-Side Benchmarks

Date: 2026-06-23

No workload benchmark has been run yet because the mirror has not started any compatible workload.

## Baseline Captured

| Runtime | Current state |
|---|---|
| Docker Desktop | production services running |
| Apple Container | 1.0.0 service running, no pilot containers |
| oMLX | healthy on `127.0.0.1:18080` |
| llama.cpp | listening on `127.0.0.1:8002` |
| Rapid-MLX | stopped |

## Benchmark Plan

For each translated workload, compare Docker Desktop production and Apple Container pilot on startup time, health latency, request latency, CPU, RSS, swap, disk growth, shutdown time, and recovery time. Native AI inference benchmarks stay separate because oMLX/llama/Rapid-MLX are not being containerized.
