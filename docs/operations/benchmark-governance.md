# Benchmark Governance

Date: 2026-06-23
Owner: AI Platform

## Purpose

Benchmark governance keeps model-lane decisions grounded in measured workload behavior on this Apple Silicon Mac.

## Metrics

| Metric | Purpose |
|---|---|
| TTFT | Interactive latency and first-token readiness |
| Output tokens/second | Decode throughput |
| Concurrency throughput | Multi-agent load behavior |
| Swap usage | System pressure and rollback trigger |
| Memory pressure | Model residency and KV/cache pressure |
| Tool-calling reliability | Agent workflow suitability |

## Recurring Benchmark Commands

Production oMLX:

```bash
LOCAL_AI_BENCH_ENGINES=omlx-mlx \
LOCAL_AI_BENCH_OUTPUT=docs/benchmarks/production-omlx-$(date -u +%Y%m%d).json \
python3 scripts/local-ai/benchmark-engine-bakeoff.py
```

Manual lab lanes:

```bash
LOCAL_AI_BENCH_ENGINES=llama-cpp-gguf \
LOCAL_AI_BENCH_OUTPUT=docs/benchmarks/lab-llama-cpp-$(date -u +%Y%m%d).json \
python3 scripts/local-ai/benchmark-engine-bakeoff.py

LOCAL_AI_BENCH_ENGINES=rapid-mlx-qwen36 \
LOCAL_AI_BENCH_OUTPUT=docs/benchmarks/lab-rapid-mlx-$(date -u +%Y%m%d).json \
python3 scripts/local-ai/benchmark-engine-bakeoff.py
```

Comparison:

```bash
scripts/operations/benchmark-governance.py \
  --baseline docs/benchmarks/post-cleanup-benchmark-results.json \
  --current docs/benchmarks/production-omlx-YYYYMMDD.json \
  --json /tmp/benchmark-comparison.json
```

## Regression Policy

| Regression | Default threshold | Action |
|---|---:|---|
| TTFT increase | 35% | Warning; repeat once before changing defaults |
| Throughput decrease | 20% | Warning; inspect memory pressure and model load state |
| Tool-call failure | any repeated failure | Candidate lane cannot be promoted |
| Swap pressure increase | high sustained pressure | Unload large models and defer lab lanes |

## Scheduling

- Monthly production oMLX benchmark.
- Quarterly lab-lane benchmark windows for llama.cpp and Rapid-MLX.
- Ad hoc benchmark before changing model defaults, engine defaults, or startup policy.

Do not run long benchmarks while swap pressure is high unless the benchmark specifically studies pressure behavior.
