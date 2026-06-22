# 07 - Benchmarks

Raw JSON: `benchmark-results.json`

## Methodology

- Same three prompts sent to both operational OpenAI-compatible endpoints.
- Streaming requests measured TTFT.
- Non-stream requests measured wall-clock latency and captured endpoint usage/timing metadata.
- Process snapshots captured RSS and CPU from `ps`.

## Results

| Engine | Workload | TTFT | Total | Output tok/s | Prompt tokens | Output tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| oMLX/MLX | coding_patch | 0.026s | 3.611s | 53.16 | 41 | 192 |
| oMLX/MLX | agent_plan | 0.003s | 3.594s | 53.43 | 36 | 192 |
| oMLX/MLX | context_scale | 0.008s | 12.129s | 15.83 | 3985 | 192 |
| llama.cpp/GGUF | coding_patch | 0.892s | 2.931s | 65.51 | 44 | 192 |
| llama.cpp/GGUF | agent_plan | 0.254s | 3.603s | 53.29 | 39 | 192 |
| llama.cpp/GGUF | context_scale | 6.213s | 3.680s | 52.17 | 3988 | 192 |

## Endpoint-Specific Notes

- llama.cpp exposes prompt/decode timings; coding prompt prefill was about `199 tok/s`, decode about `70 tok/s`.
- oMLX exposes total time and token counts but not per-token server timings in the same detail.
- llama.cpp context-scale non-stream result benefited from prompt cache; its streaming TTFT still showed high first-token latency.
- KV cache byte growth was not exposed by either active OpenAI endpoint in a portable response field; future work should enable llama.cpp metrics and add oMLX memory sampling around benchmark phases.

