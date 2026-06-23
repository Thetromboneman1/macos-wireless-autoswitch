#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

if ! command -v container >/dev/null 2>&1 || ! container system status >/dev/null 2>&1; then
  echo "Apple Container is not running; nothing to stop."
  exit 0
fi

jq -r '.services[] | select(.enabled == true) | .name' "$PORT_MAP" | while IFS= read -r name; do
  if container inspect "$name" >/dev/null 2>&1; then
    echo "Stopping pilot container: $name"
    container stop "$name" >/dev/null 2>&1 || true
  else
    echo "Pilot container not present: $name"
  fi
done
