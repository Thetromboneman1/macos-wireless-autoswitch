#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"

"$ROOT/scripts/apple-container/validate-port-map.sh"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed" >&2
  exit 1
fi

if ! container system status >/dev/null 2>&1; then
  echo "Apple Container system service is not running. Start it with: container system start" >&2
  exit 1
fi

status=0
while IFS=$'\t' read -r name url; do
  case "$url" in
    http://127.0.0.1:*)
      if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
        echo "healthy: $name $url"
      else
        echo "not running or unhealthy: $name $url"
      fi
      ;;
    *)
      echo "invalid health URL for $name: $url" >&2
      status=1
      ;;
  esac
done < <(jq -r '.services[] | [.name, .health_url] | @tsv' "$PORT_MAP")

exit "$status"
