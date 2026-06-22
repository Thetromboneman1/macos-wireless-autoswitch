# Loop 9 - Final Summary

## What Changed

- Added standard local AI entrypoints under `scripts/local-ai/`.
- Backed up and corrected host OpenCode GGUF provider URL to `127.0.0.1:8002`.
- Added this sweep artifact set and kept raw GitHub stars in `github-stars.json`.

## Installed or Configured

- No new package installs.
- Configured OpenCode host access to the existing GGUF coding lane.
- Confirmed oMLX and llama.cpp are already installed and serving.

## Engine and Model Selection

- Primary: oMLX / MLX / Metal at `127.0.0.1:18080/v1`.
- Specialist coding lane: llama.cpp / GGUF / MTP at `127.0.0.1:8002/v1`.
- Default models:
  - reasoning: `mlx-community--gemma-4-31b-it-4bit`
  - coding: `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf`
  - fast: `mlx-community--gemma-4-e4b-it-4bit`
  - routing: `mlx-community--gemma-4-e2b-it-4bit`

## GitHub Stars

- Implemented as documentation or wiring: `nvk/llm-wiki`, `google-gemma/gemma-skills`, local `llama.cpp` checkout, local Hermes/OpenCode wiring.
- Deferred: token compression/RAG/code graph/eval tools until a specific corpus or workflow is selected.

## Commit and Push Status

- Local commit target: current repo only, after final validation.
- Push status: do not push without explicit approval after the user reviews the sweep.

## Rollback

```bash
cp ~/.config/opencode/opencode.json.bak-local-ai-star-sweep-2026-06-22 ~/.config/opencode/opencode.json
scripts/local-ai/stop-default-model.sh
git revert <local-commit-sha>
```

