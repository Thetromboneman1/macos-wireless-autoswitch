#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="${1:-$ROOT/config/apple-container/port-map.json}"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to validate $PORT_MAP" >&2
  exit 2
fi

if [[ ! -f "$PORT_MAP" ]]; then
  echo "Port map not found: $PORT_MAP" >&2
  exit 2
fi

jq -e '
  . as $root
  | .schema_version == 1
  and (.policy.pilot_prefix | type == "string")
  and (.policy.reserved_range.start | type == "number")
  and (.policy.reserved_range.end | type == "number")
  and (.services | type == "array")
  and (.services | length > 0)
  and all(.services[]; (.name | startswith($root.policy.pilot_prefix)))
  and all(.services[]; .host == "127.0.0.1")
  and all(.services[]; (.host_port >= $root.policy.reserved_range.start and .host_port <= $root.policy.reserved_range.end))
  and (([.services[].host_port] | length) == ([.services[].host_port] | unique | length))
  and (([.services[].name] | length) == ([.services[].name] | unique | length))
  and ((($root.services | map(.host_port)) - $root.policy.production_ports) | length == ($root.services | map(.host_port) | length))
' "$PORT_MAP" >/dev/null

while IFS=$'\t' read -r name port; do
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Pilot port $port for $name is already listening; choose a free Apple Container pilot port." >&2
    exit 1
  fi
done < <(jq -r '.services[] | [.name, .host_port] | @tsv' "$PORT_MAP")

echo "Apple Container port map is valid and all pilot ports are free."
