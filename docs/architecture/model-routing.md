# Model Routing

Date: 2026-06-27

Machine-readable sources:

- `config/local-ai-platform/routing-policy.json`
- `config/local-ai-platform/residency-policy.json`

## Routing Principles

Use hardware and workload first, then choose the engine:

1. Apple Silicon local work starts with oMLX/MLX because it has the lowest observed TTFT and already supports the four-role Gemma contract.
2. Ornith 35B GGUF on llama.cpp is the preferred local coding lane after the 2026-06-27 benchmark, but it is on-demand rather than always resident.
3. Gemma GGUF portability, llama.cpp timing metadata, and production-simulation tests stay available on the fallback llama.cpp/llama-server lane.
4. OmniRoute and headroom are routing labs, not default front doors.
5. Ollama remains manual compatibility only.
6. Rapid-MLX is a validated specialist lane, but it refused connections during the 2026-06-27 Ornith benchmark.

## Lanes

| Lane | Engine | Model | Use |
|---|---|---|---|
| Reasoning | oMLX/MLX | `mlx-community--gemma-4-31b-it-4bit` | Architecture, planning, hard debugging, review synthesis. |
| Local coding preferred | llama.cpp | `ornith-1.0-35b-Q4_K_M.gguf` | Preferred on-demand local coding and tool-call-capable repo workflow. |
| Coding stable fallback | oMLX/MLX | `mlx-community--gemma-4-26b-a4b-it-4bit` | Stable local coding fallback and role-contract continuity. |
| GGUF coding fallback | llama.cpp | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | Portable coding fallback and llama.cpp benchmarks. |
| Rapid-MLX Qwen3.6 specialist | Rapid-MLX | `qwen3.6-35b-4bit` | Manual lab lane; stop at high swap pressure. |
| Fast agent | oMLX/MLX | `mlx-community--gemma-4-e4b-it-4bit` | Summaries, quick edits, cheap agent turns. |
| Routing utility | oMLX/MLX | `mlx-community--gemma-4-e2b-it-4bit` | Classification, routing, low-latency utilities. |

## Client Mapping

| Client | Default | Fallback |
|---|---|---|
| Codex | Cloud model plus local tools; do not force local-only. | Local oMLX for context and experiments. |
| OpenCode | Warm oMLX Gemma 26B coding model with oMLX small model configured. | Explicit Ornith 35B GGUF coding window, Gemma GGUF, and oMLX 31B roles. |
| Continue | Ornith 35B GGUF for chat/edit/apply. | oMLX Gemma roles. |
| Goose/Hermes/OpenClaw | Host tools use `127.0.0.1:18080`; Docker tools use `host.docker.internal:18080`; coding-capable Docker clients use `8003`. | Gemma GGUF `8002`, Rapid-MLX `8010` when healthy, and cloud fallback. |
| OpenHands | Use local endpoint only inside an intentional sandbox. | Cloud provider only with `Boneman` secrets. |

## Residency Rules

The active residency policy keeps oMLX `18080` warm, keeps specialist gateways listening, and allows heavy backend model processes to be stopped without treating that as drift:

| Swap state | Required listeners | Optional backend listeners |
|---|---|---|
| Normal | `18080`, `8002`, `8003`, `8010` | `18002`, `18003`, `18010` may run after tool calls. |
| High, swap used >= 80 percent | `18080`, `8002`, `8003`, `8010` | Stop `18003` Ornith and `18010` Rapid-MLX. |
| Critical, swap used >= 88 percent | `18080`, `8002`, `8003`, `8010` | Stop `18002` Gemma GGUF too. |

Use `scripts/local-ai/install-on-demand-gateways.sh` to refresh the launchd-safe installed copies, `scripts/local-ai/model-residency-governor.sh enforce` for one-shot remediation, and `com.corn.local-ai-residency-governor` for the launchd loop. Health checks must use `/__lane_status` to avoid waking cold backends.

## Benchmark Evidence

The 2026-06-27 Ornith local benchmark showed:

- Ornith 35B GGUF Q4 returned OpenAI-style `tool_calls` and separated `reasoning_content`.
- Ornith 35B GGUF Q4 produced about `57.83` output tok/s on the coding workload and about `58.21` output tok/s on the moderate-context workload.
- Gemma GGUF remains a strong fallback at about `52.20` and `54.43` output tok/s on the same workloads.
- oMLX/Gemma remains the production reasoning, fast-agent, and routing role contract.
- Rapid-MLX refused connections during this pass and should be revalidated before being treated as available.

The 2026-06-22 Hermes/MLX bake-off showed:

- oMLX/MLX TTFT remained very low and passed tool-call validation.
- llama.cpp had strong short coding decode throughput and rich timing metadata, now without MTP.
- Rapid-MLX Qwen3.6 passed tool-call validation and won the 2-way concurrency pass.
- llama.cpp exposed richer prompt/decode timing data.
- Rapid-MLX emitted a memory pressure warning for Qwen3.6 35B-A3B 4-bit on this 64 GB Mac when other services were open; keep it visible in validation results while it is left running.

See [07-benchmarks.md](../autonomous-modernization/07-benchmarks.md) and [19-hermes-mlx-implementation.md](../autonomous-modernization/19-hermes-mlx-implementation.md).

See also [35-ornith-feasibility-and-control-plane.md](../autonomous-modernization/35-ornith-feasibility-and-control-plane.md) and [benchmark-results-ornith-2026-06-27.json](../autonomous-modernization/benchmark-results-ornith-2026-06-27.json).

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
