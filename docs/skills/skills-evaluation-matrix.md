# Skills and Extension Evaluation Matrix

Date: 2026-06-23

Selection principles:

- Prefer already installed, vendor-supported, or curated tools.
- Preserve the current oMLX/MLX production lane at `http://127.0.0.1:18080/v1`.
- Keep Ollama compatibility-only unless explicitly requested.
- Avoid abandoned tools, broad-permission tools, and integrations that require secrets without a clear immediate use.
- Store credentials only in 1Password vault `Boneman`.

| Name | Source | Purpose | Install method | Maintenance status | Compatibility | Security risk | Required secrets | Status |
|---|---|---|---|---|---|---|---|---|
| `gh-address-comments` | OpenAI curated Codex skill | Address actionable PR review comments | Installed with Codex skill installer | Curated | Codex/GitHub CLI | Low; uses local repo and `gh` session | Existing `gh` auth | Install now |
| `gh-fix-ci` | OpenAI curated Codex skill | Debug failing GitHub Actions checks | Installed with Codex skill installer | Curated | Codex/GitHub CLI | Low; reads CI logs | Existing `gh` auth | Install now |
| `migrate-to-codex` | OpenAI curated Codex skill | Convert workflows into Codex-friendly form | Installed with Codex skill installer | Curated | Codex | Low | None | Install now |
| `openai-docs` | OpenAI curated/system Codex skill | OpenAI API and product documentation workflow | Installed with Codex skill installer; system skill also exists | Curated | Codex | Low | OpenAI API key only when running API examples | Already installed |
| `playwright` | OpenAI curated Codex skill | Browser validation and UI testing | Installed with Codex skill installer | Curated | Codex, VS Code task workflow | Medium; browser automation can affect local sessions | None for local tests | Install now |
| `playwright-interactive` | OpenAI curated Codex skill | Interactive browser troubleshooting | Installed with Codex skill installer | Curated | Codex | Medium; browser automation | None for local tests | Install now |
| `security-best-practices` | OpenAI curated Codex skill | Security review baseline | Installed with Codex skill installer | Curated | Codex | Low | None | Install now |
| `security-ownership-map` | OpenAI curated Codex skill | Security ownership and boundaries | Installed with Codex skill installer | Curated | Codex | Low | None | Install now |
| `security-threat-model` | OpenAI curated Codex skill | Threat modeling | Installed with Codex skill installer | Curated | Codex | Low | None | Install now |
| `yeet` | OpenAI curated Codex skill and GitHub plugin skill | Commit, push, and PR workflow | Installed with Codex skill installer; plugin skill already available | Curated | Codex/GitHub CLI | Medium; pushes code | Existing `gh` auth | Install now |
| `codex-security` plugin skills | Existing Codex plugin | Deep security scans and finding workflows | Already enabled in `~/.codex/config.toml` | Curated plugin | Codex | Medium; broad repo analysis | None unless ticketing integrations are used | Already installed |
| `github` plugin skills | Existing Codex plugin | GitHub review, CI, and publishing workflows | Already enabled in `~/.codex/config.toml` | Curated plugin | Codex/GitHub CLI | Medium; can publish if user requests | Existing `gh` auth | Already installed |
| `llm-wiki` plugin | Local Codex/OpenCode plugin | Session memory and local knowledge | Already enabled in `~/.codex/config.toml` | Local plugin | Codex/OpenCode | Low; local knowledge corpus | None | Already installed |
| `openai.chatgpt` | VS Code Marketplace | ChatGPT in VS Code | Already installed | Active marketplace extension | VS Code arm64 | Medium; external AI service if used | OpenAI account/key managed outside repo | Already installed |
| `sst-dev.opencode` | VS Code Marketplace | OpenCode editor integration | Already installed | Active marketplace extension | VS Code arm64 | Medium; agentic tool | Local provider auth through existing config | Already installed |
| `continue.continue` | VS Code Marketplace | AI coding assistant config surface | Already installed | Active marketplace extension | VS Code arm64 | Medium; model-provider access | Provider tokens if enabled; use Boneman | Already installed |
| `redhat.ansible` | VS Code Marketplace | Ansible, AAP, and automation authoring | Already installed | Vendor-supported | VS Code arm64 | Low | AAP/Satellite secrets only for live operations | Already installed |
| `redhat.vscode-yaml` | VS Code Marketplace | YAML validation and schemas | Already installed | Vendor-supported | VS Code arm64 | Low | None | Already installed |
| `github.vscode-github-actions` | VS Code Marketplace | GitHub Actions authoring | Already installed | GitHub-supported | VS Code arm64 | Low | GitHub auth for live repo actions | Already installed |
| `timonwong.shellcheck` | VS Code Marketplace | Shell diagnostics | Already installed | Active extension | VS Code arm64 | Low | None | Already installed |
| `ms-azuretools.vscode-docker` | VS Code Marketplace | Docker workflows | Already installed | Microsoft-supported | VS Code arm64 | Medium; Docker socket visibility | Registry creds if used | Already installed |
| `davidanson.vscode-markdownlint` | VS Code Marketplace | Markdown linting for docs/runbooks | Installed with VS Code CLI | Active marketplace extension | VS Code arm64 | Low | None | Install now |
| `tamasfe.even-better-toml` | VS Code Marketplace | TOML language support backed by Taplo | Installed with VS Code CLI | Preview, actively published | VS Code arm64 | Low | None | Install now |
| `ms-vscode.powershell` | VS Code Marketplace | Windows and PowerShell administration | Installed with VS Code CLI | Microsoft-supported | VS Code arm64 with PowerShell 7.6.0 | Medium when executing scripts | Windows/remote credentials if used; store in Boneman | Install now |
| `ms-kubernetes-tools.vscode-kubernetes-tools` | VS Code Marketplace | Kubernetes authoring and diagnostics | Installed with VS Code CLI | Microsoft/CNCF ecosystem | VS Code arm64 | Medium; kubeconfig access | Cluster credentials in keychain/Boneman | Install now |
| `hashicorp.terraform` | VS Code Marketplace | Terraform/HCL language support | Installed with VS Code CLI | HashiCorp-supported | VS Code arm64 | Low for editor features; medium for cloud integration | Terraform Cloud token only if used | Install now |
| `charliermarsh.ruff` | VS Code Marketplace | Python linting/formatting | Installed with VS Code CLI | Active Astral/Ruff ecosystem | VS Code arm64 | Low | None | Install now |
| `sentry` Codex skill/plugin | OpenAI curated/plugin | Sentry issue triage | Plugin enabled; curated skill not installed | Curated | Codex/Sentry | Medium; production telemetry access | Sentry token | Manual approval required |
| Notion skills | OpenAI curated skills | Notion knowledge/work tracking | Not installed | Curated | Codex/Notion | Medium; workspace access | Notion token | Manual approval required |
| Deploy skills (`vercel`, `netlify`, `cloudflare`, `render`) | OpenAI curated skills | Hosting deployment | Not installed | Curated | Codex/cloud CLIs | Medium/high; can publish externally | Provider tokens | Install later |
| Figma skills | OpenAI curated skills | Product/design workflows | Not installed | Curated | Codex/Figma | Medium; design workspace access | Figma token | Install later |
| Linear skill | OpenAI curated skill | Issue/project workflows | Not installed | Curated | Codex/Linear | Medium; project write access | Linear token | Manual approval required |
| Unknown community agent-skill bundles | GitHub community repos | Bulk community skill import | Not installed | Mixed | Mixed | High; supply-chain uncertainty | Unknown | Reject |

## Notes

- VS Code extension choices were checked against live installed versions and public marketplace/source pages on 2026-06-23.
- Codex curated skills were installed from `openai/skills` into `~/.codex/skills`.
- `taplo` was installed with Homebrew to support TOML validation.
