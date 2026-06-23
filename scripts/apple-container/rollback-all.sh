#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_ROOT="${APPLE_CONTAINER_PILOT_LOG_ROOT:-$HOME/.local/share/apple-container-pilot/logs}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_FILE="$LOG_ROOT/rollback-$STAMP.log"

mkdir -p "$LOG_ROOT"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Apple Container pilot rollback started at $STAMP"
echo "Log: $LOG_FILE"

if ! command -v container >/dev/null 2>&1; then
  echo "container CLI is not installed; nothing to stop."
  exit 0
fi

if container system status >/dev/null 2>&1; then
  pilot_count=0
  while IFS= read -r name; do
    pilot_count=$((pilot_count + 1))
    echo "Stopping pilot container: $name"
    container stop "$name" >/dev/null 2>&1 || true
    echo "Removing pilot container: $name"
    container rm "$name" >/dev/null 2>&1 || true
  done < <(container ls -a 2>/dev/null | awk 'NR > 1 && $1 ~ /^ac-/ {print $1}')
  if [[ "$pilot_count" -eq 0 ]]; then
    echo "No ac- pilot containers found."
  fi
else
  echo "Apple Container system service is stopped; skipping container cleanup."
fi

APPLE_CONTAINER_ALLOW_LISTENING=true "$ROOT/scripts/apple-container/validate-port-map.sh" || true

echo "Checking production sentinels after pilot rollback..."
curl -fsS -H "Authorization: Bearer ${OMLX_API_KEY:-mlx-local}" http://127.0.0.1:18080/health >/dev/null
if lsof -nP -iTCP:18080 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "oMLX production port 18080 is listening."
else
  echo "oMLX production port 18080 is not listening." >&2
  exit 1
fi

echo "Rollback complete. Pilot logs and data were preserved under ${LOG_ROOT%/logs}."
