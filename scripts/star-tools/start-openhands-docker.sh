#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
checkout="$ROOT/tmp/star-downloads/OpenHands__OpenHands"
workspace="${OPENHANDS_WORKSPACE_BASE:-$HOME/.local/share/codex-star-tools/workspaces/openhands}"

mkdir -p "$workspace" "$HOME/.openhands"
cd "$checkout"

export WORKSPACE_BASE="$workspace"
export AGENT_SERVER_IMAGE_REPOSITORY="${AGENT_SERVER_IMAGE_REPOSITORY:-ghcr.io/openhands/agent-server}"
export AGENT_SERVER_IMAGE_TAG="${AGENT_SERVER_IMAGE_TAG:-1.29.0-python}"

exec docker compose up "$@"
