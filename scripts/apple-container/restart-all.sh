#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

test -f "$PORT_MAP"
"$ROOT/scripts/apple-container/stop-all.sh"
"$ROOT/scripts/apple-container/start-all.sh"
