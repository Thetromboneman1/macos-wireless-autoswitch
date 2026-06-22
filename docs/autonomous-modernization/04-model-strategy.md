# 04 - Model Strategy

## Current Models

| Role | Model | Engine |
| --- | --- | --- |
| Reasoning | `mlx-community--gemma-4-31b-it-4bit` | oMLX |
| Coding default | `mlx-community--gemma-4-26b-a4b-it-4bit` | oMLX |
| Coding specialist | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | llama.cpp |
| Fast utility | `mlx-community--gemma-4-e4b-it-4bit` | oMLX |
| Routing | `mlx-community--gemma-4-e2b-it-4bit` | oMLX |

## Candidate Models

| Model | Decision |
| --- | --- |
| Gemma 4 12B Agentic Q4_K_M | Good future GGUF experiment, not pulled in this pass because 26B A4B GGUF already exists and benchmarks well. |
| Gemma 4 12B Coder Q4_K_M | Good fallback if 26B memory pressure becomes an issue. |
| Kimi-K2.7-Code-GGUF | Defer; sharded large model and license metadata require explicit approval before download. |
| Apodex models | Research/eval only. |

## Removal Decision

No models were removed. The prompt says not to keep unused models, but deletion requires a documented reason and approval. This pass only identified candidates.

