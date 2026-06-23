# VS Code Workspace Tooling

This workspace is configured for Codex, OpenCode, local AI operations, shell automation, GitHub Actions, Ansible, Docker, Kubernetes, Terraform, Python testing, Markdown, YAML, and TOML work.

## Installed User Extensions

Installed on 2026-06-23 with the VS Code app CLI:

- `davidanson.vscode-markdownlint`
- `tamasfe.even-better-toml`
- `ms-vscode.powershell`
- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `hashicorp.terraform`
- `charliermarsh.ruff`

Already present before this pass:

- `openai.chatgpt`
- `sst-dev.opencode`
- `continue.continue`
- `github.vscode-github-actions`
- `github.vscode-pull-request-github`
- `redhat.ansible`
- `redhat.vscode-yaml`
- `timonwong.shellcheck`
- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-azuretools.vscode-docker`
- `ms-azuretools.vscode-containers`
- `ms-vscode-remote.remote-containers`

## Local AI Defaults

Workspace terminals export non-secret endpoint hints:

- `LOCAL_AI_BASE_URL=http://127.0.0.1:18080/v1`
- `LOCAL_AI_CODING_BASE_URL=http://127.0.0.1:8002/v1`
- `LOCAL_AI_LAB_BASE_URL=http://127.0.0.1:8010/v1`
- `LOCAL_AI_SECRET_VAULT=Boneman`

Do not put the oMLX API key or provider credentials in workspace settings. Use `OMLX_API_KEY` at runtime or the existing `~/.omlx/settings.json`/1Password Boneman pointer flow.

## Tasks

Use the Command Palette command `Tasks: Run Task` for:

- `local-ai: health`
- `platform: status`
- `test: pytest`
- `lint: shellcheck`
- `lint: markdown`
- `validate: config`
- `security: gitleaks`

The VS Code MCP user file exists at `~/Library/Application Support/Code/User/mcp.json`, but no synthetic MCP server was added in this pass. The repo source of truth remains `config/local-ai-platform/mcp-topology.json` until a server command is validated as an MCP transport.
