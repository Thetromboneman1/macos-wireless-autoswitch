# Shared Skills Library

Date: 2026-06-23

Shared agent skills were added under:

```text
~/.agents/skills
```

## Categories

| Category | Purpose |
|---|---|
| `coding` | Repo automation, code review, CI feedback, Playwright validation, local coding model defaults |
| `devops` | CI/CD, Docker, Kubernetes, Terraform, shell, YAML, gitleaks, and platform validation |
| `macos` | LaunchAgents, plist validation, Homebrew, and macOS diagnostics |
| `local-ai` | oMLX, llama.cpp, Rapid-MLX, model roles, and endpoint verification |
| `security` | gitleaks, security skills, secret handling, and review boundaries |
| `documentation` | Markdown, runbooks, architecture docs, and OpenAI docs workflow |
| `enterprise-automation` | Ansible, AAP, Satellite, Linux, Windows, compliance, and patching workflows |

## Enterprise Agent Portfolio

Reusable enterprise copilots are documented in `docs/agents/agent-catalog.md` and integrated through `.github/prompts/enterprise-agent-workforce.prompt.md`.

| Agent | Primary skill route |
|---|---|
| Enterprise Architecture Copilot | `documentation`, `enterprise-automation`, `security` |
| AAP Platform Copilot | `enterprise-automation`, `devops`, `security` |
| Satellite Platform Copilot | `enterprise-automation`, `devops`, `security` |
| Server Engineering Copilot | `devops`, `enterprise-automation`, `security` |
| Executive Communications Copilot | `documentation` plus the relevant domain skill |
| Automation Discovery Copilot | `enterprise-automation`, `documentation` |
| Operational Review Copilot | `devops`, `documentation`, `local-ai`, `security` |

## Design

The shared skills are lightweight routing skills. They do not duplicate full Codex skill bodies and they do not contain secrets. Their job is to keep local agents aligned on:

- the oMLX production endpoint;
- the four Gemma role model IDs;
- the no-Ollama-by-default rule;
- the Boneman vault requirement;
- repo validation commands;
- installed Codex skills that should be reused.

## Maintenance

When a new shared skill is added:

1. Put it under the closest category in `~/.agents/skills`.
2. Keep `SKILL.md` short and operational.
3. Reference validated commands and docs.
4. Store any required secret in 1Password vault `Boneman`.
5. Update this document and `docs/skills/skills-evaluation-matrix.md`.
