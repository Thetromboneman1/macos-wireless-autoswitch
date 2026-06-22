# 19 - Hermes MLX Implementation

Date: 2026-06-22

## Installed And Downloaded

- Installed `rapid-mlx 0.8.10` with `uv tool install --force rapid-mlx@latest`.
- Downloaded `mlx-community/Qwen3.6-35B-A3B-4bit` through `rapid-mlx pull qwen3.6-35b-4bit`.
- Cached model path: `~/.cache/huggingface/hub/models--mlx-community--Qwen3.6-35B-A3B-4bit/snapshots/38740b847e4cb78f352aba30aa41c76e08e6eb46`.

## Configured

- Hermes host CLI primary config now points to `http://127.0.0.1:18080/v1`.
- Hermes default model is `mlx-community--gemma-4-26b-a4b-it-4bit`.
- Added Rapid-MLX lab launcher: `scripts/local-ai/start-rapid-mlx-qwen.sh`.
- Added rollback helper: `scripts/local-ai/rollback-hermes-mlx.sh`.
- Added reusable endpoint validator: `scripts/local-ai/validate-hermes-mlx.py`.
- Updated GGUF launcher to remove Apple Silicon MTP flags.

## Validation Results

Raw validation artifacts:

- `docs/autonomous-modernization/hermes-mlx-validation-omlx.json`
- `docs/autonomous-modernization/hermes-mlx-validation-rapid-mlx.json`
- `docs/autonomous-modernization/benchmark-results.json`

| Endpoint | Model | Models | Chat | Tool call |
|---|---|---:|---:|---:|
| oMLX | `mlx-community--gemma-4-26b-a4b-it-4bit` | pass | pass | pass |
| Rapid-MLX | `qwen3.6-35b-4bit` | pass | pass | pass |

Hermes CLI one-shot validation was attempted after setting the host endpoint and model. It returned `API call failed after 3 retries: Connection error.` The endpoint-level validations above prove the local OpenAI-compatible servers work, so the remaining issue is in Hermes' provider/auth/config path rather than oMLX or Rapid-MLX serving.

## Benchmark Takeaways

| Engine | Short coding tok/s | Moderate context tok/s | 2-way aggregate tok/s | Takeaway |
|---|---:|---:|---:|---|
| oMLX Gemma 26B-A4B | 44.29 | 20.27 | 15.39 | Best stable default with very low TTFT. |
| llama.cpp Gemma 26B-A4B GGUF | 52.73 | 39.34 | 16.82 | Best timing visibility and strong decode, now no-MTP. |
| Rapid-MLX Qwen3.6 35B-A3B | 36.75 | 16.07 | 32.51 | Best 2-way concurrency and tool-call candidate; memory headroom warning means lab/default-candidate, not always-on default. |

## Known Limits

- Rapid-MLX warned that Qwen3.6-35B-A3B 4-bit can exceed comfortable memory pressure on this 64 GB Mac when other large local services are open.
- The first uncached Rapid-MLX stream was slow during benchmark warmup, while cached/non-stream calls were much faster.
- Hermes CLI one-shot still needs a follow-up pass for its auth/provider path even though direct endpoint validation passes.
- Ollama is not installed in PATH, so it was not benchmarked.
- Lightning MLX was not installed because its current public path emphasizes MTP/MTPLX, which conflicts with the PDF rule for this Mac.

## Rollback

```bash
scripts/local-ai/rollback-hermes-mlx.sh
```

This stops Rapid-MLX and the optional GGUF lane and prints the oMLX default configuration.
