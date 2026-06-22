# Star Deployment Implementation

Date: 2026-06-22

## Summary

This pass implemented the recommended starred repositories from the deferred-star reassessment. Download size, model size, storage, and bandwidth were not used as blockers. The remaining safety boundary is operational: services that can proxy credentials, grant broad filesystem access, or alter agent behavior are installed and launchable, but not autostarted.

## Installed And Deployed

| Repo | Deployment | Validation |
|---|---|---|
| `StarTrail-org/LEANN` | `uv tool install --python 3.13 leann-core --with leann`; installs `leann` and `leann_mcp` in `~/.local/bin`. | `leann --help` succeeds. |
| `RyjoxTechnologies/Octopoda-OS` | `uv tool install --python 3.13 'octopoda[server,mcp,ai]'`; installs `octopoda`, `octopoda-mcp`, `octopoda-run`, and helpers. | `octopoda --help` succeeds. |
| `TheStageAI/edge-lm` | Isolated uv env at `~/.local/share/codex-star-tools/envs/edge-lm`; editable install from local checkout. | `import edge_lm`; MLX `0.31.2`; Python `3.13.13`. |
| `beamivalice/PonyExl3` | Isolated uv env at `~/.local/share/codex-star-tools/envs/ponyexl3`; editable install from local checkout using Python `3.14`. | `import ponyexl3`; MLX `0.31.2`; Python `3.14.3`. |
| `RyanCodrai/turbovec` | Isolated uv env at `~/.local/share/codex-star-tools/envs/turbovec`; PyPI install on Python `3.12`. | Import/search smoke test succeeds. |
| `kennss/SiliconScope` | SwiftPM build of `sscope-cli` in `tmp/star-downloads/kennss__SiliconScope/.build/debug/sscope-cli`. | One-sample no-sudo hardware probe succeeds. |
| `nvk/llm-wiki` | Registered as local Codex marketplace source; enabled `[plugins."wiki@llm-wiki"]`; OpenCode instruction path added. | Config checks pass; headless Codex verifier reports pending until interactive `/plugins` enables first materialization. |
| `Egonex-AI/Understand-Anything` | Local installer cloned to `~/.understand-anything/repo`, linked skills into `~/.agents/skills`, installed pnpm deps. | Symlink and dependency checks pass. |
| `diegosouzapw/OmniRoute` | Installed Node dependencies in `tmp/star-downloads/diegosouzapw__OmniRoute/node_modules`; guarded local start script added. | Dependency directory present; earlier npm dry-run and current install succeeded. |
| `headroomlabs-ai/headroom` | Built release `headroom-proxy` from Rust workspace. | `headroom-proxy --help` succeeds. |
| `OpenHands/OpenHands` | Synced uv environment and pulled `ghcr.io/openhands/agent-server:1.29.0-python`. | Docker image present; uv sync completed. |

## Installed Footprint

| Path | Size |
|---|---:|
| `~/.local/share/codex-star-tools/envs/turbovec` | 25 MB |
| `tmp/star-downloads/kennss__SiliconScope/.build` | 221 MB |
| `~/.local/share/codex-star-tools/envs/ponyexl3` | 302 MB |
| `~/.understand-anything/repo` | 624 MB |
| `~/.local/share/codex-star-tools/envs/edge-lm` | 708 MB |
| `~/.local/share/uv/tools/octopoda` | 709 MB |
| `~/.local/share/uv/tools/leann-core` | 1.1 GB |
| `tmp/star-downloads/OpenHands__OpenHands/.venv` | 1.1 GB |
| `tmp/star-downloads/headroomlabs-ai__headroom/target` | 1.1 GB |
| `tmp/star-downloads/diegosouzapw__OmniRoute/node_modules` | 2.0 GB |
| `ghcr.io/openhands/agent-server:1.29.0-python` | 1.44 GB |

## Run Commands

| Tool | Command |
|---|---|
| Validate all deployments | `scripts/star-tools/validate-star-deployments.sh` |
| Octopoda local dashboard | `scripts/star-tools/start-octopoda-local.sh` |
| headroom proxy | `scripts/star-tools/start-headroom-proxy.sh http://127.0.0.1:18080` |
| OmniRoute isolated local app | `scripts/star-tools/start-omniroute-local.sh` |
| OpenHands Docker app | `scripts/star-tools/start-openhands-docker.sh` |
| Understand-Anything dashboard | `scripts/star-tools/start-understand-dashboard.sh` |
| Rollback reference | `scripts/star-tools/rollback-star-deployments.sh` |

## Config Changes

Backups were created before editing user config:

```text
~/.local/share/codex-star-tools/backups/20260622-150120/
```

Changed config:

- `~/.codex/config.toml`
  - Added `[marketplaces.llm-wiki]` pointing to the local `nvk/llm-wiki` checkout.
  - Added `[plugins."wiki@llm-wiki"] enabled = true`.
- `~/.config/opencode/opencode.json`
  - Added local `llm-wiki` OpenCode instruction file.
  - Added external directory permissions for `~/.config/llm-wiki/**`, `~/wiki/**`, and the iCloud wiki path.
- `~/.agents/skills`
  - Added Understand-Anything skill symlinks.

## Safety Notes

- No LaunchAgents or autostart daemons were added.
- No cloud API keys, OAuth tokens, or provider credentials were created, printed, or stored.
- OmniRoute, headroom, and OpenHands are installed but stopped by default.
- headroom compression is off unless explicitly enabled.
- OpenHands is configured through the upstream Docker Compose path and should be run only when the workspace mount is intentional.
- `llm-wiki` may require opening Codex `/plugins` once to complete first-time plugin materialization.

## Validation Results

`scripts/star-tools/validate-star-deployments.sh` passed after installation.

Highlights:

- LEANN CLI and MCP command are installed.
- Octopoda CLI and MCP command are installed.
- edge-lm imports with MLX.
- PonyExl3 imports with MLX on Python 3.14.
- turbovec can create an index and return a nearest-neighbor result.
- SiliconScope can sample Apple Silicon telemetry without sudo.
- headroom proxy binary is built and runnable.
- OpenHands agent-server image is present locally.
- llm-wiki Codex/OpenCode config is present.
- Understand-Anything symlinks and dependencies are present.
- OmniRoute dependencies are present.

## Not Autostarted

The following are intentionally not running as background services:

- OmniRoute, because it can become a provider routing layer and may manage API/OAuth credentials.
- headroom, because it is a proxy and should be attached to a deliberate upstream.
- OpenHands, because the agent-server workflow can grant broad workspace/filesystem access.
- Octopoda, because it writes local agent memory/audit state and should be started per experiment.

## Rollback

Run:

```bash
scripts/star-tools/rollback-star-deployments.sh
```

The script prints targeted rollback commands rather than removing anything automatically. Use the specific command for the component you want to remove.
