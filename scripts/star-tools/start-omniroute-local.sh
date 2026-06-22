#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
checkout="$ROOT/tmp/star-downloads/diegosouzapw__OmniRoute"
state="${OMNIROUTE_DATA_DIR:-$HOME/.local/share/codex-star-tools/state/omniroute}"

mkdir -p "$state"
cd "$checkout"

export DATA_DIR="$state"
export HOSTNAME="${HOSTNAME:-127.0.0.1}"
export PORT="${PORT:-20128}"
export REQUIRE_API_KEY="${REQUIRE_API_KEY:-false}"
export ALLOW_API_KEY_REVEAL="${ALLOW_API_KEY_REVEAL:-false}"

exec npm run dev "$@"
