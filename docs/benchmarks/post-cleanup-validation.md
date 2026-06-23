# Post-Cleanup Benchmark Validation

Date: 2026-06-23

Benchmark artifact:

```text
docs/benchmarks/post-cleanup-benchmark-results.json
```

## Scope

The post-cleanup benchmark sampled only the production oMLX lane. llama.cpp and Rapid-MLX remained stopped because phase two prioritized memory reduction and startup simplification.

## Results

| Workload | TTFT | Output tok/s | RSS delta |
|---|---:|---:|---:|
| coding patch | 0.049s | 46.54 | 0 KiB |
| agent plan | 0.003s | 46.96 | 16 KiB |
| context scale | 0.005s | 33.71 | 480 KiB |
| moderate context | 0.008s | 29.35 | -192 KiB |
| 2-way concurrency | n/a | 24.31 aggregate | 256 KiB |

## Comparison

Compared with the earlier oMLX benchmark summary in `docs/autonomous-modernization/07-benchmarks.md`, TTFT stayed low and memory growth remained negligible. Short decode throughput improved versus the previous oMLX sample, while 2-way aggregate throughput was effectively unchanged.

## Cleanup Action

After the benchmark, `scripts/omlx-power-policy.sh unload-large` unloaded the primary/coding models. oMLX remained healthy and model memory reported `0`.

## Lab Lane Revalidation

llama.cpp and Rapid-MLX should be revalidated only during a dedicated benchmark window:

```bash
LOCAL_AI_BENCH_ENGINES=llama-cpp-gguf LOCAL_AI_BENCH_OUTPUT=docs/benchmarks/post-cleanup-llama-cpp.json python3 scripts/local-ai/benchmark-engine-bakeoff.py
LOCAL_AI_BENCH_ENGINES=rapid-mlx-qwen36 LOCAL_AI_BENCH_OUTPUT=docs/benchmarks/post-cleanup-rapid-mlx.json python3 scripts/local-ai/benchmark-engine-bakeoff.py
```
