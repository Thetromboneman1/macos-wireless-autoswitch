# 07 - Benchmarks

Raw JSON:

- `benchmark-results.json`
- `benchmark-results-omlx-extended.json`
- `benchmark-results-llama-cpp-extended.json`
- `benchmark-results-rapid-mlx-extended.json`
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
| oMLX/MLX | coding_patch | 0.034s | 2.877s | 33.36 | 0.030s | 41 | 96 |
| oMLX/MLX | agent_plan | 0.005s | 3.052s | 31.46 | 0.032s | 36 | 96 |
| oMLX/MLX | context_scale | 0.012s | 2.772s | 34.64 | 0.029s | 1365 | 96 |
| oMLX/MLX | context_moderate | 0.008s | 3.246s | 29.57 | 0.034s | 3587 | 96 |
| llama.cpp/GGUF no-MTP | coding_patch | 0.330s | 2.528s | 37.98 | 0.026s | 44 | 96 |
| llama.cpp/GGUF no-MTP | agent_plan | 0.291s | 2.504s | 38.34 | 0.026s | 39 | 96 |
| llama.cpp/GGUF no-MTP | context_scale | 2.834s | 2.981s | 32.20 | 0.031s | 1368 | 96 |
| llama.cpp/GGUF no-MTP | context_moderate | 7.203s | 2.387s | 40.23 | 0.025s | 3590 | 96 |
| Rapid-MLX/Qwen3.6 | coding_patch | 0.083s | 1.619s | 59.30 | 0.017s | 38 | 96 |
| Rapid-MLX/Qwen3.6 | agent_plan | 0.003s | 1.609s | 59.66 | 0.017s | 33 | 96 |
| Rapid-MLX/Qwen3.6 | context_scale | 0.004s | 1.679s | 57.16 | 0.017s | 1282 | 96 |
| Rapid-MLX/Qwen3.6 | context_moderate | 0.007s | 5.668s | 16.94 | 0.059s | 3405 | 96 |

## Concurrency

| Engine | Concurrency | Aggregate output tok/s | Wall time | Aggregate output tokens | RSS delta |
|---|---:|---:|---:|---:|---:|
| oMLX/MLX | 2 | 23.65 | 5.412s | 128 | -39,104 KiB |
| llama.cpp/GGUF no-MTP | 2 | 18.00 | 7.111s | 128 | -278,464 KiB |
| Rapid-MLX/Qwen3.6 | 2 | 35.17 | 3.639s | 128 | 4,176 KiB |

## Endpoint-Specific Notes

- oMLX remains the stable default because it passed tool-call validation and has consistently low TTFT.
- llama.cpp is now explicitly no-MTP and exposes prompt/decode timings; the coding prompt reported about `206 tok/s` prompt processing and `58.7 tok/s` predicted decode.
- llama.cpp won the short coding non-stream pass.
- Rapid-MLX won the 2-way concurrency pass and passed tool-call validation with Qwen3.6-35B-A3B.
- Rapid-MLX emitted a memory pressure warning for this 64 GB Mac during startup, so it remains a lab/default-candidate lane rather than an always-on default.
- RSS deltas are noisy because both engines cache and release memory between requests; treat them as pressure signals, not exact KV-cache byte accounting.
