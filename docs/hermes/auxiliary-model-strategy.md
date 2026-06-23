# Hermes Auxiliary Model Strategy

Date: 2026-06-23
Owner: Platform Operations

## Current Model Roles

| Role | Model | Backend | Decision |
|---|---|---|---|
| Primary/default coding | `mlx-community--gemma-4-26b-a4b-it-4bit` | oMLX | Keep. |
| Reasoning | `mlx-community--gemma-4-31b-it-4bit` | oMLX | Keep. |
| Fast auxiliary | `mlx-community--gemma-4-e4b-it-4bit` | oMLX | Keep. |
| Routing/utility | `mlx-community--gemma-4-e2b-it-4bit` | oMLX | Keep. |
| GGUF coding lane | `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` | llama.cpp | Manual lane. |
| Rapid-MLX candidate | `qwen3.6-35b-4bit` | Rapid-MLX | Manual lab lane. |

## Compression Model

Hermes currently uses `mlx-community--gemma-4-e4b-it-4bit` as `compression.summary_model`.

This is acceptable for now because compression is enabled conservatively and no compression failure was observed in this pass. It is not yet proven for every long-session payload. Before promoting a different compression model, run:

- summary-quality test;
- factual-retention test;
- long-context test;
- tool-loop preservation test;
- privacy review.

## Rejected

Do not download or select uncensored models solely because a Reddit comment recommends them. Schema following, context capacity, and privacy matter more than anecdotal creativity for this stack.
