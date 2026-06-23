# Skills Installation and Integration

Date: 2026-06-23

## Summary

This pass installed and wired a conservative, high-utility tooling set for Codex, VS Code, local agents, local AI operations, security review, GitHub Actions, macOS automation, DevOps, and enterprise automation.

The current local AI architecture was preserved:

- production: oMLX at `http://127.0.0.1:18080/v1`;
- default coding model: `mlx-community--gemma-4-26b-a4b-it-4bit`;
- experimental: Rapid-MLX at `http://127.0.0.1:8010/v1`;
- reliability/specialist: llama.cpp at `http://127.0.0.1:8002/v1`;
- secrets: 1Password vault `Boneman`.

No secret values were written to repo files.

## Installed

Codex skills:

- `gh-address-comments`
- `gh-fix-ci`
- `migrate-to-codex`
- `openai-docs`
- `playwright`
- `playwright-interactive`
- `security-best-practices`
- `security-ownership-map`
- `security-threat-model`
- `yeet`

VS Code extensions:

- `charliermarsh.ruff`
- `davidanson.vscode-markdownlint`
- `hashicorp.terraform`
- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `ms-vscode.powershell`
- `tamasfe.even-better-toml`

Shared agent skills:

- `coding`
- `devops`
- `macos`
- `local-ai`
- `security`
- `documentation`
- `enterprise-automation`

Validation tool:

- `taplo`

## Configured

Repo files:

- `.vscode/extensions.json`
- `.vscode/settings.json`
- `.vscode/tasks.json`
- `.vscode/local-ai.code-snippets`
- `.vscode/README.md`
- `AGENTS.md`

User files:

- `~/Library/Application Support/Code/User/settings.json`
- `~/.agents/skills/*/SKILL.md`
- `~/.codex/skills/*`

Documentation:

- `docs/skills/skills-evaluation-matrix.md`
- `docs/skills/installed-skills.md`
- `docs/skills/codex-skills.md`
- `docs/skills/vscode-skills-and-extensions.md`
- `docs/skills/shared-skills-library.md`
- `docs/security/secret-inventory.md`
- `docs/security/onepassword-secrets.md`

## Deferred or Manual Approval Required

- Sentry skill: defer until a Sentry token and project boundary are explicitly approved.
- Notion skills: defer until workspace scope is approved.
- Deployment skills for Vercel, Netlify, Cloudflare, and Render: install later only when a deployment target is active.
- Figma and design skills: install later for product design work.
- Bulk community skill repositories: rejected for this pass because maintenance and supply-chain quality vary widely.

## Validation Plan

Run before publishing:

```bash
'/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code' --list-extensions --show-versions
find /Users/corn/.codex/skills -maxdepth 2 -type f -name SKILL.md
find /Users/corn/.agents/skills -maxdepth 3 -type f -name SKILL.md
jq empty .vscode/*.json config/local-ai-platform/*.json
jq empty "/Users/corn/Library/Application Support/Code/User/settings.json"
taplo check /Users/corn/.codex/config.toml
plutil -lint launchd/*.plist com.computernetworkbasics.wifionoff.plist
shellcheck install.sh wireless.sh scripts/**/*.sh
markdownlint README.md docs/**/*.md
uvx pytest
gitleaks detect --no-banner --redact --source .
curl -sS http://127.0.0.1:18080/health
curl -sS -H "Authorization: Bearer $(jq -r '.auth.api_key' /Users/corn/.omlx/settings.json)" http://127.0.0.1:18080/v1/models
```
