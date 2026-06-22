# Loop 2 - Inference Engine Decision

## Evidence

- Apple M1 Max, 64 GB unified memory, Metal 4.
- oMLX `0.4.4` CLI and app are running and expose all four Gemma MLX role models on `127.0.0.1:18080`.
- llama.cpp build `ebc10770a`, version `9614`, is serving the existing 26B A4B GGUF/MTP lane on `127.0.0.1:8002`.
- Docker Desktop is available but has about 8 GB container memory and no Metal path for Linux model serving.
- OpenCode can see both `gguf-coding/...` and `omlx/...` providers.

## Decision

| Role | Choice | Why |
| --- | --- | --- |
| Primary engine | oMLX / MLX / Metal | Best match for Apple Silicon, already running, clean OpenAI-compatible API, preserves existing four-role Gemma contract. |
| Specialist coding lane | llama.cpp / llama-server GGUF/MTP | Already running, fast, reversible, supports GGUF-only models and MTP draft acceleration. |
| Fallback engine | LM Studio or Ollama/manual llama.cpp | Useful for GUI/manual testing or model-card one-offs; not the automated default. |
| GUI/manual tool | LM Studio | Installed and useful for manual GGUF exploration without changing production agents. |
| Not chosen | vLLM | Not mature enough for this Apple Silicon host path compared with native MLX and llama.cpp Metal. |
| Not chosen | Docker Model Runner as primary | Docker cannot provide Metal acceleration on this Mac and container memory is too low for the main models. |

## Default Models

- Primary reasoning: `mlx-community--gemma-4-31b-it-4bit`.
- Coding workhorse: `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` on llama.cpp.
- Fast agent: `mlx-community--gemma-4-e4b-it-4bit`.
- Routing/utility: `mlx-community--gemma-4-e2b-it-4bit`.
- Optional future small GGUF: Gemma 4 12B agentic `Q4_K_M`.

## Rollback

- Stop GGUF lane: `scripts/local-ai/stop-default-model.sh`.
- Restore OpenCode config: copy back `~/.config/opencode/opencode.json.bak-local-ai-star-sweep-2026-06-22`.
- Keep oMLX on localhost and app-managed unless a separate LaunchAgent decision is approved.

