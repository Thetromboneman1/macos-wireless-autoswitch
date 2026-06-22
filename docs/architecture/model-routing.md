# Model Routing

Date: 2026-06-22

Machine-readable source: `config/local-ai-platform/routing-policy.json`.

## Routing Principles

Use hardware and workload first, then choose the engine:

1. Apple Silicon local work starts with oMLX/MLX because it has the lowest observed TTFT and already supports the four-role Gemma contract.
2. GGUF portability, llama.cpp timing metadata, and production-simulation tests go to llama.cpp/llama-server.
3. OmniRoute and headroom are routing labs, not default front doors.
4. Ollama remains manual compatibility only.

## Lanes

| Lane | Engine | Model | Use |
|---|---|---|---|
| Reasoning | oMLX/MLX | `mlx-community--gemma-4-31b-it-4bit` | Architecture, planning, hard debugging, review synthesis. |
| Coding default | oMLX/MLX | `mlx-community--gemma-4-26b-a4b-it-4bit` | Main local coding workflow. |
| GGUF coding specialist | llama.cpp | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | Portable coding lane and llama.cpp benchmarks. |
| Fast agent | oMLX/MLX | `mlx-community--gemma-4-e4b-it-4bit` | Summaries, quick edits, cheap agent turns. |
| Routing utility | oMLX/MLX | `mlx-community--gemma-4-e2b-it-4bit` | Classification, routing, low-latency utilities. |

## Client Mapping

| Client | Default | Fallback |
|---|---|---|
| Codex | Cloud model plus local tools; do not force local-only. | Local oMLX for context and experiments. |
| OpenCode | GGUF coding model with oMLX small model configured. | oMLX 26B/31B roles. |
| Goose/Hermes/OpenClaw | Use oMLX endpoint policy when edited. | Keep cloud fallback. |
| OpenHands | Use local endpoint only inside an intentional sandbox. | Cloud provider only with `Boneman` secrets. |

## Benchmark Evidence

The 2026-06-22 bake-off showed:

- oMLX/MLX TTFT was lower on all measured prompts.
- llama.cpp had stronger short coding decode throughput.
- llama.cpp exposed richer prompt/decode timing data.
- KV cache byte growth still needs a dedicated metrics pass.

See [07-benchmarks.md](../autonomous-modernization/07-benchmarks.md).

## Router Lab Rules

OmniRoute may become the unified provider router only after:

- provider credential storage is mapped to `Boneman`,
- request logging and API-key reveal behavior are disabled or controlled,
- default local routing is proven no worse than direct oMLX/llama.cpp calls,
- rollback is a single config change back to direct endpoints.

headroom may become a compression layer only after:

- compression quality and latency are benchmarked,
- no sensitive prompt logging is enabled,
- token discovery paths are reviewed,
- upstream fallback behavior is documented.
