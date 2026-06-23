#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

test -f "$PORT_MAP"
if "$ROOT/scripts/apple-container/health-all.sh"; then
  echo "All enabled Apple Container pilot services are healthy."
  exit 0
fi

echo "Repairing enabled Apple Container pilot services with bounded restart."
"$ROOT/scripts/apple-container/restart-all.sh"
