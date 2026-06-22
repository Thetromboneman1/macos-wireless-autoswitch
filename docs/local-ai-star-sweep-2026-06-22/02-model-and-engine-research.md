# Loop 1b - Model and Engine Research

## Known in 5 bullets

- oMLX already serves the four local Gemma MLX role models.
- A llama.cpp build already serves Gemma 4 26B A4B GGUF/MTP on `127.0.0.1:8002`.
- Disk has about 1.2 TiB free, but Kimi GGUF is multi-part and not practical to pull blindly.
- Docker Desktop cannot expose Apple Metal to Linux containers, so model serving belongs on the host.
- Q4-class quants remain the default practical choice unless benchmarks prove otherwise.

## Hugging Face Sources

| Source | Evidence | Decision |
| --- | --- | --- |
| `yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF` | Apache-2.0, updated 2026-06-19, offers `Q3_K_M`, `Q4_K_M`, `Q6_K`, `Q8_0`, recommends `Q4_K_M`, llama.cpp/OpenAI-compatible usage, notes `--jinja`, repetition penalty, and temperature guidance | Good optional small agentic GGUF. Do not replace the existing faster/larger 26B A4B lane without benchmark need. |
| `yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF` | Apache-2.0, updated 2026-06-19, has `Q2_K`, `Q3_K_M`, `Q4_K_M`, `Q6_K`, `Q8_0` | Good fallback coder candidate; default to `Q4_K_M` if later downloaded. |
| `unsloth/Kimi-K2.7-Code-GGUF` | Updated 2026-06-19, license marked `other`, large multi-file GGUF shards across many quants | Document-only for this Mac. Pull only after explicit approval and a size/time plan. |
| `apodex/apodex-1` collection | Contains `Apodex-1.0-mini`, `4B-SFT`, `2B-SFT`, `0.8B-SFT`; paired star `ApodexAI/AgentHarness` is an eval harness | Useful for eval research, not an immediate serving replacement. |
| `llm-wiki.net` / `nvk/llm-wiki` | Supports Claude Code, Codex, OpenCode, Pi, and AGENTS.md-style agents; focuses on compiled knowledge bases and source ingestion | High-value documentation/knowledge-base candidate; defer install until a specific wiki target is chosen. |

## Quant Notes

- Gemma 4 12B agentic: `Q3_K_M` is smallest reliable option per model card; `Q4_K_M` is the sweet spot; `Q6_K`/`Q8_0` are quality-first.
- Gemma 4 12B coder: `Q4_K_M` should be first candidate if adding a lighter coder lane.
- Existing 26B A4B GGUF lane uses `UD-Q4_K_XL`, draft MTP, Metal offload, flash attention, 65k context, and is already validated locally.

## Links

- https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF
- https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF
- https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF
- https://huggingface.co/collections/apodex/apodex-1
- https://llm-wiki.net/

