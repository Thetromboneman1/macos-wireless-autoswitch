#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

APPLE_CONTAINER_ALLOW_LISTENING=true "$ROOT/scripts/apple-container/validate-port-map.sh"

status=0
jq -c '.services[] | select(.enabled == true)' "$PORT_MAP" | while IFS= read -r service; do
  name="$(jq -r '.name' <<<"$service")"
  url="$(jq -r '.health_url' <<<"$service")"
  if curl -fsS --max-time 10 "$url" >/dev/null 2>&1; then
    echo "healthy: $name $url"
  else
    echo "unhealthy: $name $url" >&2
    status=1
  fi
  exit "$status"
done
