# VS Code Skills and Extensions

Date: 2026-06-23

## Workspace Files

Created:

- `.vscode/extensions.json`
- `.vscode/settings.json`
- `.vscode/tasks.json`
- `.vscode/local-ai.code-snippets`
- `.vscode/README.md`

Updated user settings:

- `~/Library/Application Support/Code/User/settings.json`

## Extension Coverage

| Workflow | Extension support |
|---|---|
| Codex workflows | `openai.chatgpt`, repo tasks, snippets, Codex skills |
| OpenCode/local AI | `sst-dev.opencode`, `continue.continue`, local endpoint settings |
| GitHub Actions | `github.vscode-github-actions` |
| PR review | `github.vscode-pull-request-github`, `eamodio.gitlens` |
| YAML | `redhat.vscode-yaml` |
| Markdown | `davidanson.vscode-markdownlint` |
| Shell | `timonwong.shellcheck`, `foxundermoon.shell-format` |
| Python | `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff` |
| Docker | `ms-azuretools.vscode-docker`, `ms-azuretools.vscode-containers` |
| Dev containers | `ms-vscode-remote.remote-containers` |
| Ansible/AAP | `redhat.ansible` |
| Kubernetes | `ms-kubernetes-tools.vscode-kubernetes-tools` |
| Terraform/IaC | `hashicorp.terraform` |
| TOML | `tamasfe.even-better-toml`, `taplo` CLI |
| Windows administration | `ms-vscode.powershell`, `pwsh` |

## Tasks

Workspace tasks expose:

- local AI health checks
- platform status checks
- pytest
- ShellCheck
- Markdown linting
- JSON/TOML validation
- gitleaks

## MCP

VS Code user MCP config exists at:

```text
~/Library/Application Support/Code/User/mcp.json
```

No new MCP server command was added because the repo does not currently expose a validated VS Code MCP transport command. Keep using `config/local-ai-platform/mcp-topology.json` as the topology source of truth until a server command is validated.
