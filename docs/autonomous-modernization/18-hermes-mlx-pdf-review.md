# 18 - Hermes MLX PDF Review

Date: 2026-06-22

Primary source: `/Users/corn/Downloads/Mac + MLX Megathread — Hermes Agent on Apple Silicon (June 2026) : r:hermesagent.pdf`.

## Extracted Decision Rules

- Do not enable MTP on Apple Silicon. The PDF calls out MTP on Metal as a net loss and specifically warns against `--spec-type draft-mtp`.
- Validate `/v1/chat/completions` with tool calls before trusting a backend for Hermes.
- Prefer MLX/oMLX or Rapid-MLX for Apple Silicon speed and MoE generation.
- Prefer llama.cpp when KV cache control, GGUF portability, vision/mmproj, Jinja templates, and timing visibility matter.
- Treat Ollama as convenience only, LM Studio as optional GUI support, and Lightning MLX as a lab lane until its MTP-centered path is proven safe here.
- Start conservative on context, then benchmark upward.
- For 64 GB Apple Silicon, test Qwen3.6-35B-A3B 4-bit and keep Gemma 4 26B-A4B/31B/E4B/E2B as the existing cross-family contract.

## Local Hardware Fit

This Mac is an Apple M1 Max MacBook Pro with 64 GB RAM, macOS 26.5.1, and about 1.2 TB free disk at audit time. That fits the PDF's 48-64 GB lane, but the live Rapid-MLX server warned that Qwen3.6-35B-A3B 4-bit can exceed comfortable memory headroom when other large local stacks are open.

## Backend Implications

| Backend | PDF guidance | Local decision |
|---|---|---|
| oMLX / MLX | Strong Apple Silicon default. | Keep as primary default because it already serves the four Gemma roles and passed tool-call validation. |
| Rapid-MLX | Best new tool-calling candidate. | Installed `rapid-mlx 0.8.10`, downloaded Qwen3.6-35B-A3B 4-bit, validated as a lab lane on `127.0.0.1:8010`. |
| llama.cpp | Best control/compatibility path. | Keep optional GGUF lane, but remove MTP flags. |
| Lightning MLX | Fast agentic fork. | Document only for now because its public path emphasizes MTP/MTPLX. |
| Ollama | Convenience layer. | Not installed in PATH; no default role. |
| LM Studio | GUI support. | Running as GUI; not default automation backend. |

## Resulting Default

Default Hermes host CLI endpoint:

```text
base_url: http://127.0.0.1:18080/v1
model: mlx-community--gemma-4-26b-a4b-it-4bit
provider: custom
api_mode: chat_completions
```

Rapid-MLX Qwen3.6 is now the best candidate to keep testing for Hermes orchestration, but oMLX Gemma 26B-A4B is the safer always-on default because it passed validation without the Rapid-MLX memory warning.
