# Local AI Platform Runbook

Date: 2026-06-22

## Daily Status

```bash
scripts/star-tools/platform-status.sh
```

For deeper checks:

```bash
scripts/star-tools/validate-star-deployments.sh
scripts/health/local-ai-health.py
```

## Start Optional Services

Start only what the current task needs:

```bash
scripts/star-tools/start-octopoda-local.sh
scripts/star-tools/start-understand-dashboard.sh
scripts/star-tools/start-headroom-proxy.sh http://127.0.0.1:18080
scripts/star-tools/start-omniroute-local.sh
scripts/star-tools/start-openhands-docker.sh
```

## Normal Routing

- Default model endpoint: `http://127.0.0.1:18080/v1`.
- GGUF coding lane: `http://127.0.0.1:8002/v1`, no MTP.
- Rapid-MLX Hermes candidate: `http://127.0.0.1:8010/v1`, start only with `scripts/local-ai/start-rapid-mlx-qwen.sh`.
- Do not route routine work through OmniRoute or headroom until their lab reviews pass.

## Config Consumers

These user and workspace configs are wired to the shared policy files:

| Consumer | Config |
|---|---|
| Codex | `~/.codex/config.toml` |
| OpenCode | `~/.config/opencode/opencode.json` |
| Goose | `~/.config/goose/config.yaml` |
| Hermes | `~/.hermes/config.yaml` |
| Hermes WebUI | `~/.hermes/webui/settings.json` |
| Hermes WebUI MVP | `~/.hermes/webui-mvp/settings.json` |
| VS Code user settings | `~/Library/Application Support/Code/User/settings.json` |
| Hermes workspace VS Code | `~/Documents/Hermes/.vscode/settings.json` |
| OpenClaw workspace VS Code | `~/Documents/Openclaw/.vscode/settings.json` |

Backups from the 2026-06-22 platform wiring pass are stored under:

```text
~/.local/share/codex-star-tools/backups/20260622-161103-platform-configs/
```

## Secret Handling

- Canonical vault: `Boneman`.
- The duplicate `Boneman Projects` vault was empty and removed on 2026-06-22.
- Do not paste secrets into docs, scripts, `.env.example`, or git commits.
- Prefer runtime env vars populated from 1Password or existing local settings.

## Hermes Host Endpoint Rule

Hermes running on the macOS host must use loopback endpoints:

```text
oMLX: http://127.0.0.1:18080/v1
GGUF: http://127.0.0.1:8002/v1
```

Use `host.docker.internal` only for Docker consumers. The 2026-06-23 Hermes RCA found that host-side `host.docker.internal` entries caused the CLI to retry until `API call failed after 3 retries: Connection error`.

## OpenHands

Use OpenHands only with an intentional workspace:

```bash
OPENHANDS_WORKSPACE_BASE="$HOME/.local/share/codex-star-tools/workspaces/openhands" \
  scripts/star-tools/start-openhands-docker.sh
```

Stop with:

```bash
(cd tmp/star-downloads/OpenHands__OpenHands && docker compose down)
```

## Router Lab

OmniRoute:

```bash
REQUIRE_API_KEY=true scripts/star-tools/start-omniroute-local.sh
```

headroom:

```bash
HEADROOM_PROXY_COMPRESSION=0 scripts/star-tools/start-headroom-proxy.sh http://127.0.0.1:18080
```

Keep `ALLOW_API_KEY_REVEAL=false` for OmniRoute.

## Knowledge Layer

Use llm-wiki for curated local AI references. Use LEANN and Understand-Anything when a repo needs semantic or graph-based context. Do not index secret-bearing paths.

## Recovery

Rollback guidance:

```bash
scripts/star-tools/rollback-star-deployments.sh
```

This prints targeted removal commands rather than deleting anything automatically.

If an optional service is misbehaving:

1. Stop the service process or Docker Compose stack.
2. Re-run `scripts/star-tools/platform-status.sh`.
3. Use direct oMLX/llama.cpp endpoints until the router/proxy issue is resolved.

## Release Hygiene

Before committing:

```bash
scripts/star-tools/platform-status.sh
scripts/star-tools/validate-star-deployments.sh
jq . config/local-ai-platform/routing-policy.json >/dev/null
jq . config/local-ai-platform/mcp-topology.json >/dev/null
git diff --check
git diff | grep -Ei 'secret|token|password|apikey|api_key|private_key|BEGIN RSA|BEGIN OPENSSH' || true
```

Inspect secret-scan hits manually; policy text and placeholders are acceptable, real values are not.
