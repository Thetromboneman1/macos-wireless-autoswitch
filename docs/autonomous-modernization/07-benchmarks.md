# 07 - Benchmarks

Raw JSON:

- `benchmark-results.json`
- `benchmark-results-omlx-extended.json`
- `benchmark-results-llama-cpp-extended.json`
- `hermes-mlx-validation-omlx.json`
- `hermes-mlx-validation-rapid-mlx.json`

## Methodology

- Same prompts sent to operational OpenAI-compatible endpoints.
- Streaming requests measured TTFT.
- Non-stream requests measured wall-clock latency and captured endpoint usage/timing metadata.
- Process snapshots captured RSS and CPU from `ps`.
- Extended pass adds moderate context scaling, RSS deltas as a KV/cache pressure proxy, and 2-way concurrency.

## Extended Results

| Engine | Workload | TTFT | Total | Output tok/s | TPOT | Prompt tokens | Output tokens |
|---|---|---:|---:|---:|---:|---:|---:|
| oMLX/MLX | coding_patch | 0.029s | 2.167s | 44.29 | 0.023s | 41 | 96 |
| oMLX/MLX | agent_plan | 0.007s | 2.922s | 32.86 | 0.030s | 36 | 96 |
| oMLX/MLX | context_scale | 0.033s | 4.692s | 20.46 | 0.049s | 1365 | 96 |
| oMLX/MLX | context_moderate | 0.021s | 4.737s | 20.27 | 0.049s | 3587 | 96 |
| llama.cpp/GGUF no-MTP | coding_patch | 0.922s | 1.821s | 52.73 | 0.019s | 44 | 96 |
| llama.cpp/GGUF no-MTP | agent_plan | 0.213s | 1.832s | 52.40 | 0.019s | 39 | 96 |
| llama.cpp/GGUF no-MTP | context_scale | 0.153s | 2.379s | 40.35 | 0.025s | 1368 | 96 |
| llama.cpp/GGUF no-MTP | context_moderate | 0.212s | 2.441s | 39.34 | 0.025s | 3590 | 96 |
| Rapid-MLX/Qwen3.6 | coding_patch | 0.104s | 2.612s | 36.75 | 0.027s | 38 | 96 |
| Rapid-MLX/Qwen3.6 | agent_plan | 0.015s | 1.822s | 52.70 | 0.019s | 33 | 96 |
| Rapid-MLX/Qwen3.6 | context_scale | 0.012s | 1.866s | 51.43 | 0.019s | 1282 | 96 |
| Rapid-MLX/Qwen3.6 | context_moderate | 0.015s | 5.975s | 16.07 | 0.062s | 3405 | 96 |

## Concurrency

| Engine | Concurrency | Aggregate output tok/s | Wall time | Aggregate output tokens | RSS delta |
|---|---:|---:|---:|---:|---:|
| oMLX/MLX | 2 | 15.39 | 8.317s | 128 | -27,504 KiB |
| llama.cpp/GGUF no-MTP | 2 | 16.82 | 7.612s | 128 | 278,720 KiB |
| Rapid-MLX/Qwen3.6 | 2 | 32.51 | 3.938s | 128 | 28,400 KiB |

## Endpoint-Specific Notes

- oMLX remains the stable default because it passed tool-call validation and has consistently low TTFT.
- llama.cpp is now explicitly no-MTP and exposes prompt/decode timings; the coding prompt reported about `206 tok/s` prompt processing and `58.7 tok/s` predicted decode.
- llama.cpp won the short coding non-stream pass.
- Rapid-MLX won the 2-way concurrency pass and passed tool-call validation with Qwen3.6-35B-A3B.
- Rapid-MLX emitted a memory pressure warning for this 64 GB Mac during startup, so it remains a lab/default-candidate lane rather than an always-on default.
- RSS deltas are noisy because both engines cache and release memory between requests; treat them as pressure signals, not exact KV-cache byte accounting.
