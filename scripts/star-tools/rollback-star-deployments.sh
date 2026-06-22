#!/usr/bin/env bash
set -euo pipefail

cat <<'ROLLBACK'
Star deployment rollback commands:

  uv tool uninstall leann-core
  uv tool uninstall octopoda
  rm -rf ~/.local/share/codex-star-tools/envs/edge-lm
  rm -rf ~/.local/share/codex-star-tools/envs/ponyexl3
  rm -rf ~/.local/share/codex-star-tools/envs/turbovec
  rm -rf tmp/star-downloads/kennss__SiliconScope/.build
  rm -rf tmp/star-downloads/headroomlabs-ai__headroom/target
  rm -rf tmp/star-downloads/diegosouzapw__OmniRoute/node_modules
  rm -rf tmp/star-downloads/OpenHands__OpenHands/.venv
  docker image rm ghcr.io/openhands/agent-server:1.29.0-python
  ~/.understand-anything/repo/install.sh --uninstall codex
  ~/.understand-anything/repo/install.sh --uninstall opencode
  rm -rf ~/.understand-anything ~/.understand-anything-plugin

Restore backed-up config files from:
  ~/.local/share/codex-star-tools/backups/$(cat ~/.local/share/codex-star-tools/backups/latest)

Manual config cleanup:
  - Remove [marketplaces.llm-wiki] and [plugins."wiki@llm-wiki"] from ~/.codex/config.toml
  - Remove the llm-wiki instruction path and external_directory entries from ~/.config/opencode/opencode.json

This script prints commands only. Run the specific rollback command you need.
ROLLBACK
