# Agent Instructions

This repository is part of the local AI and macOS automation stack on this Apple Silicon Mac.

## Local AI Defaults

- Production OpenAI-compatible endpoint: `http://127.0.0.1:18080/v1`.
- Production engine: oMLX/MLX.
- Default coding model: `mlx-community--gemma-4-26b-a4b-it-4bit`.
- Reasoning model: `mlx-community--gemma-4-31b-it-4bit`.
- Fast-agent model: `mlx-community--gemma-4-e4b-it-4bit`.
- Routing/utility model: `mlx-community--gemma-4-e2b-it-4bit`.
- llama.cpp coding lane: `http://127.0.0.1:8002/v1`, no MTP by default.
- Rapid-MLX lab lane: `http://127.0.0.1:8010/v1`, manual/experimental only.

Do not replace oMLX with Ollama or another default unless fresh benchmark evidence shows the new route is better for the workload.

## Secrets

- Store secrets in 1Password vault `Boneman`.
- Do not use `Boneman Projects`, `BonemanP Projects`, or `Bonema Project Vault`.
- Document secret item names, retrieval methods, and rotation guidance only.
- Never commit secret values, token prefixes, cookies, private keys, or raw credential files.

## Validation

Use targeted checks for the files changed:

```bash
uvx pytest
shellcheck install.sh wireless.sh scripts/**/*.sh
markdownlint README.md docs/**/*.md
jq empty config/local-ai-platform/*.json .vscode/*.json
taplo check /Users/corn/.codex/config.toml
gitleaks detect --no-banner --redact --source .
```

When validating local AI, check host health, authenticated `/v1/models`, and a tiny chat completion before claiming the stack is usable.
