# Production Model Catalog

Date: 2026-06-27

## Current Ranking

| Rank | Category | Winner | Reason |
|---:|---|---|---|
| 1 | Best Local Coding | Ornith 1.0 35B Q4 GGUF on llama.cpp | Best measured local coding throughput in the 2026-06-27 benchmark and tool-call validation passed. |
| 2 | Best Stable Overall | Gemma 4 26B-A4B on oMLX | Stable production endpoint, strong coding fallback, low TTFT, Hermes verified. |
| 3 | Best GGUF Fallback | Gemma 4 26B-A4B GGUF on llama.cpp | Strong decode and useful timing metadata; keep as reliability lane. |
| 4 | Best Tool Calling | Ornith 1.0 35B Q4 GGUF on llama.cpp | Forced OpenAI tool-call schema returned parsed `tool_calls`. |
| 5 | Best Hermes | Gemma 4 26B-A4B on oMLX | Hermes one-shot now returns `OK.` after host endpoint fix. |
| 6 | Best Orchestration | Gemma 4 E2B/E4B on oMLX | Best fit for routing, summaries, and fast utility turns. |
| 7 | Best Low Memory | Gemma 4 E2B on oMLX | Small routing/utility role with low latency. |
| 8 | Best Long Context | llama.cpp reliability lanes | Best place to test explicit context/KV/cache settings before production use. |
| 9 | Best Multimodal | Not promoted | Vision/mmproj remains a lab task. |

## Catalog

| Model | Backend | Lane | Strengths | Weaknesses | Production Suitability |
|---|---|---|---|---|---|
| `ornith-1.0-35b-Q4_K_M.gguf` | llama.cpp | Preferred on-demand local coding | Strong local coding throughput, tool calls, reasoning parser output, 65k context configured | Reasoning-first responses need larger `max_tokens`; separate process adds memory pressure | Promoted as preferred on-demand local coding candidate |
| `mlx-community--gemma-4-26b-a4b-it-4bit` | oMLX/MLX | Stable production | Coding, repo automation, Hermes orchestration, tool calls | Less timing detail than llama.cpp | Production default |
| `mlx-community--gemma-4-31b-it-4bit` | oMLX/MLX | Reasoning | Architecture, planning, review synthesis | Higher memory cost | Production selectable, not always loaded |
| `mlx-community--gemma-4-e4b-it-4bit` | oMLX/MLX | Fast agent | Summaries, quick edits, cheaper turns | Lower reasoning depth | Production utility |
| `mlx-community--gemma-4-e2b-it-4bit` | oMLX/MLX | Routing utility | Classification, routing, health pings | Not a deep coding model | Production utility |
| `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | llama.cpp | Reliability/lab | Strong coding throughput, timing visibility, portability | Separate process, no Apple Silicon MTP | Lab and fallback |
| `qwen3.6-35b-4bit` | Rapid-MLX | Experimental | High throughput and concurrency candidate | Memory pressure risk | Lab only |
| `deepreinforce-ai/Ornith-1.0-397B` | Remote vLLM/SGLang | Candidate | Strong advertised agentic coding and tool-calling target | Not feasible locally on 64 GB unified memory; requires approved remote 8x80 GB-class GPU deployment | Blocked, not promoted |
| `mlx-community--Qwen3.6-35B-A3B-4bit` | Hugging Face cache | Experimental | Available locally for Qwen testing | Needs controlled benchmark pass | Lab only |
| `mlx-community--Qwen3.6-27B-OptiQ-4bit` | Hugging Face lock/cache reference | Experimental | Candidate OptiQ lane | Not fully benchmarked in this pass | Not promoted |
| `google/gemma-4-12b` | LM Studio cache | Lab | Smaller Gemma candidate | Not wired into production endpoint | Not promoted |

## Benchmark Standard

Every model promotion requires:

- authenticated `/v1/models`;
- chat completion;
- structured output or forced tool-call check;
- TTFT and output tok/s;
- context scaling;
- 2-way concurrency;
- RSS and swap delta;
- Hermes one-shot if intended for Hermes;
- rollback path.
