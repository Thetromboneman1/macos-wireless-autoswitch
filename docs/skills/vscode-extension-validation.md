# VS Code Extension Validation

Date: 2026-06-23

## Scope

Validate that the VS Code extensions installed in the skills integration pass are present and supported by workspace recommendations, settings, and tasks.

Expected installed extensions:

- `charliermarsh.ruff`
- `davidanson.vscode-markdownlint`
- `hashicorp.terraform`
- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `ms-vscode.powershell`
- `tamasfe.even-better-toml`

## Commands

```bash
'/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code' --list-extensions --show-versions
jq empty .vscode/extensions.json .vscode/settings.json .vscode/tasks.json .vscode/local-ai.code-snippets
scripts/health/local-ai-health.py --skip-chat --json /tmp/local-ai-health.json
jq '.vscode_recommendations' /tmp/local-ai-health.json
```

## Result

Installed versions observed:

| Extension | Version |
|---|---|
| `charliermarsh.ruff` | `2026.54.0` |
| `davidanson.vscode-markdownlint` | `0.61.2` |
| `hashicorp.terraform` | `2.39.3` |
| `ms-kubernetes-tools.vscode-kubernetes-tools` | `1.4.0` |
| `ms-vscode.powershell` | `2025.4.0` |
| `tamasfe.even-better-toml` | `0.21.2` |

Workspace coverage:

- recommendations: `.vscode/extensions.json`;
- settings: `.vscode/settings.json`;
- tasks: `.vscode/tasks.json`;
- local AI snippets: `.vscode/local-ai.code-snippets`.

## Workflow Support

| Workflow | Validation support |
|---|---|
| Markdown docs | `markdownlint` extension and CLI |
| TOML/Codex config | Even Better TOML plus `taplo` |
| PowerShell/Windows admin | PowerShell extension plus `pwsh` |
| Kubernetes | Kubernetes Tools |
| Terraform/IaC | HashiCorp Terraform extension |
| Python health tooling | Ruff extension plus `uvx pytest` |

No VS Code MCP server was added in this pass. The repo topology source of truth remains `config/local-ai-platform/mcp-topology.json`.
