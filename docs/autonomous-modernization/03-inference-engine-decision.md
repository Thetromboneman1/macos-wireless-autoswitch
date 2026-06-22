# 03 - Inference Engine Decision

## Facts

- Hardware: Apple M1 Max, 64 GB unified memory, Metal 4.
- Workload: Codex/OpenCode/Hermes-style coding, planning, long-context repo summaries, Docker consumers over host boundary.
- Operational candidates: oMLX/MLX at `127.0.0.1:18080`, llama.cpp at `127.0.0.1:8002`.
- Avoid defaulting to Ollama; keep it as manual compatibility only.

## Benchmark Decision

| Workload | oMLX / MLX | llama.cpp / GGUF |
| --- | ---: | ---: |
| coding patch output tok/s | 53.16 | 65.51 |
| agent plan output tok/s | 53.43 | 53.29 |
| context-scale output tok/s | 15.83 | 52.17 warm-cache wall result |
| coding patch TTFT | 0.026s | 0.892s |
| agent plan TTFT | 0.003s | 0.254s |
| context-scale TTFT | 0.008s | 6.213s |

## Selection

| Role | Winner | Reason |
| --- | --- | --- |
| Best Engine | oMLX/MLX for default local agent stack | Lower TTFT, native Mac behavior, already handles four-role Gemma contract. |
| Best Coding Throughput | llama.cpp GGUF/MTP | Higher decode speed on the main short coding prompt and excellent GGUF portability. |
| Best Fallback | llama.cpp | Most portable for GGUF model-card experiments. |
| Best Developer Experience | oMLX + OpenCode provider | Least friction for existing OpenCode/Hermes role mapping. |
| Best Production Simulation | llama-server | Explicit OpenAI-compatible API, model-card compatible flags, and rich timing metadata. |

## Final Policy

Use oMLX/MLX as the default agent front door and keep llama.cpp as the specialist coding lane. Do not replace the MLX default with llama.cpp until a broader benchmark shows llama.cpp wins under uncached long-context and multi-session behavior.

