# Codex Skills

Date: 2026-06-23

## Current Codex Configuration

Audited:

- `~/.codex/config.toml`
- `~/.codex/skills`
- `~/.codex/AGENTS.md`
- plugin state exposed in `~/.codex/config.toml`

Important enabled plugins include:

- `github@openai-curated`
- `codex-security@openai-curated`
- `circleci@openai-curated`
- `sentry@openai-curated`
- `openai-developers@openai-curated`
- `build-macos-apps@openai-curated`
- `build-ios-apps@openai-curated`
- `wiki@llm-wiki`
- `documents`, `spreadsheets`, and `presentations` from the primary runtime

## Added Skills

The following skills were installed from `openai/skills`:

- `gh-address-comments`: GitHub PR feedback handling.
- `gh-fix-ci`: GitHub Actions failure triage.
- `migrate-to-codex`: Codex workflow migration.
- `openai-docs`: OpenAI docs workflow.
- `playwright`: browser validation.
- `playwright-interactive`: interactive browser debugging.
- `security-best-practices`: security review baseline.
- `security-ownership-map`: ownership and boundary mapping.
- `security-threat-model`: threat modeling.
- `yeet`: publish workflow for commit/push/PR tasks.

## Local AI Contract

Codex should preserve these local defaults for this repository:

- oMLX production front door: `http://127.0.0.1:18080/v1`.
- Reasoning: `mlx-community--gemma-4-31b-it-4bit`.
- Coding: `mlx-community--gemma-4-26b-a4b-it-4bit`.
- Fast agent: `mlx-community--gemma-4-e4b-it-4bit`.
- Routing/utility: `mlx-community--gemma-4-e2b-it-4bit`.
- llama.cpp specialist lane: `http://127.0.0.1:8002/v1`.
- Rapid-MLX lab lane: `http://127.0.0.1:8010/v1`.

Do not move the default to Ollama without benchmark evidence and explicit user approval.

## Secret Handling

Codex workflows that need credentials must use 1Password vault `Boneman`.

Do not use:

- `Boneman Projects`
- `BonemanP Projects`
- `Bonema Project Vault`

Document item names and retrieval methods only.
