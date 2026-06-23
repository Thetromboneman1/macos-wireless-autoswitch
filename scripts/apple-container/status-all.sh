#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

APPLE_CONTAINER_ALLOW_LISTENING=true "$ROOT/scripts/apple-container/status.sh"

echo
echo "== Enabled pilot services =="
jq -r '.services[] | select(.enabled == true) | [.name, .host_port, .status, .health_url] | @tsv' "$PORT_MAP"
