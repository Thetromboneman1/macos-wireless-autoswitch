#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT_MAP="$ROOT/config/apple-container/port-map.json"
PILOT_ROOT="${APPLE_CONTAINER_PILOT_ROOT:-$HOME/.local/share/apple-container-pilot}"
REPORT_DIR="$PILOT_ROOT/evidence"
REPORT="$REPORT_DIR/self-heal-$(date -u +%Y%m%dT%H%M%SZ).json"
MAX_ATTEMPTS="${APPLE_CONTAINER_REPAIR_ATTEMPTS:-3}"

mkdir -p "$REPORT_DIR"

attempt=1
while [[ "$attempt" -le "$MAX_ATTEMPTS" ]]; do
  if "$ROOT/scripts/apple-container/health-all.sh"; then
    jq -n --arg status "healthy" --argjson attempts "$attempt" --arg port_map "$PORT_MAP" '{status:$status,attempts:$attempts,port_map:$port_map}' | tee "$REPORT"
    exit 0
  fi
  echo "Self-heal attempt $attempt of $MAX_ATTEMPTS"
  "$ROOT/scripts/apple-container/repair-all.sh" || true
  sleep "$attempt"
  attempt=$((attempt + 1))
done

"$ROOT/scripts/apple-container/logs-all.sh" > "$REPORT_DIR/self-heal-last-logs.txt" 2>&1 || true
"$ROOT/scripts/apple-container/stop-all.sh" || true
curl -fsS -H "Authorization: Bearer ${OMLX_API_KEY:-mlx-local}" http://127.0.0.1:18080/health >/dev/null
jq -n --arg status "failed" --argjson attempts "$MAX_ATTEMPTS" --arg port_map "$PORT_MAP" '{status:$status,attempts:$attempts,port_map:$port_map,production_omlx:"healthy"}' | tee "$REPORT"
exit 1
