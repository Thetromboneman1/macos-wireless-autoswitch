# Agent Instructions

This repository owns macOS Wi-Fi auto-switching and its direct LaunchDaemon
support. It does not own the local AI platform.

## Repository Boundary

- Keep wireless switching, dock/undock networking, installer logic, and related
  macOS automation here.
- Put local AI runtime, model routing, model residency, agent-platform, Apple
  Container pilot, benchmark, and platform-governance work in
  `/Users/corn/Documents/Boneman_Projects`.
- Do not add new oMLX, GGUF, Rapid-MLX, MCP, or agent-platform runtime files to
  this repository.

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
gitleaks detect --no-banner --redact --source .
```
