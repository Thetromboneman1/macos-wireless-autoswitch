# 07 - Benchmarks

Raw JSON:

- `benchmark-results.json`
- `benchmark-results-omlx-extended.json`
- `benchmark-results-llama-cpp-extended.json`

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
| oMLX/MLX | context_moderate | 0.008s | 3.246s | 29.58 | 0.034s | 3587 | 96 |
| llama.cpp/GGUF | coding_patch | 0.330s | 2.528s | 37.98 | 0.026s | 44 | 96 |
| llama.cpp/GGUF | agent_plan | 0.291s | 2.504s | 38.34 | 0.026s | 39 | 96 |
| llama.cpp/GGUF | context_scale | 2.834s | 2.981s | 32.20 | 0.031s | 1368 | 96 |
| llama.cpp/GGUF | context_moderate | 7.203s | 2.387s | 40.23 | 0.025s | 3590 | 96 |

## Concurrency

| Engine | Concurrency | Aggregate output tok/s | Wall time | Aggregate output tokens | RSS delta |
|---|---:|---:|---:|---:|---:|
| oMLX/MLX | 2 | 23.65 | 5.412s | 128 | -39,104 KiB |
| llama.cpp/GGUF | 2 | 18.00 | 7.111s | 128 | -278,464 KiB |

## Endpoint-Specific Notes

- oMLX still wins first-token latency by a large margin.
- llama.cpp exposes prompt/decode timings; the coding prompt reported about `172 tok/s` prompt processing and `41.7 tok/s` predicted decode.
- llama.cpp decode throughput won the short coding prompt and moderate-context non-stream pass.
- llama.cpp context prompts showed much higher streaming TTFT, especially the moderate-context prompt at about `7.2s`.
- RSS deltas are noisy because both engines cache and release memory between requests; treat them as pressure signals, not exact KV-cache byte accounting.
