# Ornith Feasibility And Control Plane

Date: 2026-06-27

## Decision

Do not download or attempt to run `deepreinforce-ai/Ornith-1.0-397B` on this Mac.

The full 397B model is a remote-GPU candidate, not a practical Apple Silicon local model on the current machine. The local Ornith path is `Ornith-1.0-35B-GGUF` Q4_K_M on llama.cpp at `http://127.0.0.1:8003/v1`; the production oMLX/Gemma role contract remains the stable fallback and non-coding role set.

## Evidence

Current Mac audit:

| Signal | Observed |
|---|---|
| Model | MacBook Pro `MacBookPro18,2` |
| Chip | Apple M1 Max |
| CPU/GPU | 10 CPU cores, 32 GPU cores |
| Unified memory | 64 GB |
| macOS | 26.5.1 |
| Metal | Metal 4 |
| Available storage | about 1.2 TiB |
| Swap during audit | `10240.00M` total, `9241.88M` used |

Official model metadata checked on 2026-06-27:

| Repo | Revision | Files | Repository size |
|---|---|---:|---:|
| `deepreinforce-ai/Ornith-1.0-397B` | `5e3e761811e804c295c1d3c0ce68b21da6154209` | 136 | 793,633,331,312 bytes |
| `deepreinforce-ai/Ornith-1.0-397B-FP8` | `8b61f97a8512d9d01bff1a9625c9a16730e115bb` | 136 | 405,183,264,091 bytes |
| `deepreinforce-ai/Ornith-1.0-35B-GGUF` Q4_K_M | `c2e1703039380de4ce6820e97afd185682d3c16c` | 1 model file plus metadata | 21,166,757,760 bytes for Q4_K_M |

The BF16 config reports `Qwen3_5MoeForConditionalGeneration`, `dtype: bfloat16`, 60 text layers, 512 experts, 10 experts per token, and `262144` max position embeddings. The FP8 repo uses `compressed-tensors` FP8 quantization.

The upstream model card says the OpenAI-compatible serving recipes use recent vLLM or SGLang and stand up the service on a single `8x80GB` GPU node with tensor parallelism 8. It also requires Qwen3-compatible reasoning and tool-call parsers for correct `reasoning_content` and `tool_calls`.

## Memory Estimate

Minimum weight-only estimates for 397B parameters:

| Precision | Weight-only estimate |
|---|---:|
| BF16 | about 739.48 GiB |
| FP16 | about 739.48 GiB |
| FP8 / 8-bit | about 369.74 GiB |
| 6-bit | about 277.31 GiB |
| 5-bit | about 231.09 GiB |
| 4-bit | about 184.87 GiB |

These numbers do not include KV cache, runtime memory, graph/workspace overhead, OS memory, Docker/editor pressure, or long-context working set. Even an ideal 4-bit full-weight local load is far beyond 64 GB unified memory. The official FP8 repository is also far beyond local memory.

## Tier Selection

| Tier | Result | Reason |
|---|---|---|
| Tier 1, full 397B locally | Rejected | Memory is insufficient by multiple factors before overhead. Swap-heavy loading would not be a valid deployment. |
| Tier 2, full 397B remote | Viable with approval | Requires 8x80 GB-class GPU capacity, auth, TLS/private networking, spend controls, and validation. |
| Tier 3, best local Ornith | Implemented | `ornith-1.0-35b-Q4_K_M.gguf` is installed, benchmarked, and wired as preferred on-demand local coding candidate. |

## Desired State

The machine-readable desired state is `config/local-ai-platform/ornith-desired-state.json`.

Current policy:

- Provider name: `ornith`.
- Primary alias: `ornith-primary`.
- Local fallback alias: `ornith-local`.
- Full model: `deepreinforce-ai/Ornith-1.0-397B`.
- Local fallback today: `ornith-1.0-35b-Q4_K_M.gguf` on `http://127.0.0.1:8003/v1` when explicitly started, with current oMLX/Gemma production stack preserved as stable fallback.
- Embeddings: keep a separate embedding model.
- Secrets: 1Password vault `Boneman`.
- Tool rewiring: completed for OpenCode, Continue, OpenClaw, Odysseus, and platform metadata; Goose keeps oMLX as its single OpenAI host and records Ornith metadata.

## Activation Gates

Before Ornith becomes the default for Codex, OpenCode, Hermes, Goose, OpenClaw, containers, or aliases:

1. `/v1/models` must return the exact Ornith model id or approved served alias.
2. A minimal chat completion must succeed.
3. `reasoning_content` must be separated from final content.
4. OpenAI `tool_calls` must parse correctly.
5. The endpoint must not silently fall back to another model.
6. Latency, memory, and reliability must be documented.
7. The existing oMLX/Gemma fallback must still work.

## Approval Boundary

Do not create paid cloud GPU resources, provision remote inference, expose a public endpoint, or store new remote credentials without explicit approval.

After approval, the preferred implementation is a private vLLM or SGLang endpoint with:

- authentication and TLS or private networking;
- Qwen3 reasoning and tool-call parsers;
- prefix or prompt caching where available;
- bounded retries and request timeouts;
- usage accounting with secret redaction;
- automatic shutdown or spend limits;
- persistent Hugging Face cache;
- rollback to the current oMLX/Gemma provider.

## Current Blockers

- No approved remote GPU host or spend boundary.
- No remote API key or private network endpoint.
- No local full 397B path; use the validated 35B GGUF lane locally.
- `agent-reach` skill is installed, but the `agent-reach` CLI was not on PATH during this pass; web evidence was collected through Hugging Face APIs instead.
