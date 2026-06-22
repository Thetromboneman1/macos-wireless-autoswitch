# Model Routing

Date: 2026-06-22

Machine-readable source: `config/local-ai-platform/routing-policy.json`.

## Routing Principles

Use hardware and workload first, then choose the engine:

1. Apple Silicon local work starts with oMLX/MLX because it has the lowest observed TTFT and already supports the four-role Gemma contract.
2. GGUF portability, llama.cpp timing metadata, and production-simulation tests go to llama.cpp/llama-server.
3. OmniRoute and headroom are routing labs, not default front doors.
4. Ollama remains manual compatibility only.
5. Rapid-MLX is a validated Hermes lab lane for Qwen3.6 tool-calling, not the always-on default.

## Lanes

| Lane | Engine | Model | Use |
|---|---|---|---|
| Reasoning | oMLX/MLX | `mlx-community--gemma-4-31b-it-4bit` | Architecture, planning, hard debugging, review synthesis. |
| Coding default | oMLX/MLX | `mlx-community--gemma-4-26b-a4b-it-4bit` | Main local coding workflow. |
| GGUF coding specialist | llama.cpp | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | Portable coding lane and llama.cpp benchmarks. |
| Rapid-MLX Hermes candidate | Rapid-MLX | `qwen3.6-35b-4bit` | Tool-calling and concurrency lab lane on demand. |
| Fast agent | oMLX/MLX | `mlx-community--gemma-4-e4b-it-4bit` | Summaries, quick edits, cheap agent turns. |
| Routing utility | oMLX/MLX | `mlx-community--gemma-4-e2b-it-4bit` | Classification, routing, low-latency utilities. |

## Client Mapping

| Client | Default | Fallback |
|---|---|---|
| Codex | Cloud model plus local tools; do not force local-only. | Local oMLX for context and experiments. |
| OpenCode | GGUF coding model with oMLX small model configured. | oMLX 26B/31B roles. |
| Goose/Hermes/OpenClaw | Host tools use `127.0.0.1:18080`; Docker tools use `host.docker.internal:18080`. | Rapid-MLX `8010` lab lane and cloud fallback. |
| OpenHands | Use local endpoint only inside an intentional sandbox. | Cloud provider only with `Boneman` secrets. |

## Benchmark Evidence

The 2026-06-22 Hermes/MLX bake-off showed:

- oMLX/MLX TTFT remained very low and passed tool-call validation.
- llama.cpp had strong short coding decode throughput and rich timing metadata, now without MTP.
- Rapid-MLX Qwen3.6 passed tool-call validation and won the 2-way concurrency pass.
- llama.cpp exposed richer prompt/decode timing data.
- Rapid-MLX emitted a memory pressure warning for Qwen3.6 35B-A3B 4-bit on this 64 GB Mac when other services were open.

See [07-benchmarks.md](../autonomous-modernization/07-benchmarks.md) and [19-hermes-mlx-implementation.md](../autonomous-modernization/19-hermes-mlx-implementation.md).

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
