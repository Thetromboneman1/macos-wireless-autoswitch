#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLICY_SCRIPT="$SCRIPT_DIR/omlx-power-policy.sh"
STATE_FILE="${OMLX_POWER_STATE_FILE:-$HOME/.omlx/power-policy-state}"
INTERVAL_SECONDS="${OMLX_POWER_WATCH_INTERVAL:-60}"

current_source() {
  if pmset -g batt | head -n 1 | grep -qi "Battery Power"; then
    printf '%s\n' "battery"
  else
    printf '%s\n' "normal"
  fi
}

apply_if_changed() {
  local source="$1"
  local previous=""
  if [ -f "$STATE_FILE" ]; then
    previous="$(cat "$STATE_FILE" 2>/dev/null || true)"
  fi

  if [ "$source" = "$previous" ]; then
    return
  fi

  mkdir -p "$(dirname "$STATE_FILE")"
  "$POLICY_SCRIPT" "$source"
  printf '%s\n' "$source" > "$STATE_FILE"
  echo "Applied oMLX $source policy."
}

if [ "${1:-}" = "--once" ]; then
  apply_if_changed "$(current_source)"
  exit 0
fi

while true; do
  apply_if_changed "$(current_source)"
  sleep "$INTERVAL_SECONDS"
done
