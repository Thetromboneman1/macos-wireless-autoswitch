#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bin="$ROOT/tmp/star-downloads/headroomlabs-ai__headroom/target/release/headroom-proxy"
listen="${HEADROOM_PROXY_LISTEN:-127.0.0.1:8787}"
upstream="${1:-${HEADROOM_PROXY_UPSTREAM:-}}"

if [ -z "$upstream" ]; then
  cat >&2 <<'USAGE'
Usage: scripts/star-tools/start-headroom-proxy.sh <upstream-base-url>

Example:
  scripts/star-tools/start-headroom-proxy.sh http://127.0.0.1:18080

Compression is off by default. Set HEADROOM_PROXY_COMPRESSION=1 only for
intentional proxy experiments.
USAGE
  exit 2
fi

exec "$bin" --listen "$listen" --upstream "$upstream" "${@:2}"
