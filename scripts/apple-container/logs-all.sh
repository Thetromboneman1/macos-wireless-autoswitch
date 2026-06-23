#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed" >&2
  exit 1
fi

jq -r '.services[] | select(.enabled == true) | .name' "$PORT_MAP" | while IFS= read -r name; do
  echo "== $name =="
  container logs -n 80 "$name" || true
done
